from fastapi import APIRouter
from pydantic import BaseModel
from difflib import get_close_matches

from app.data.store_data import PRODUCTS, STORE_INFO
from app.services.llm_service import generate_llm_response

router = APIRouter()

# Estado por usuario (simple, en memoria)
user_states = {}

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"  # si querés después lo cambiamos

# --- Utilidades ---

def corregir_palabra(palabra, opciones):
    match = get_close_matches(palabra.lower(), opciones, n=1, cutoff=0.6)
    return match[0] if match else palabra

def buscar_producto_por_nombre(texto):
    texto = texto.lower()
    for p in PRODUCTS:
        if p["nombre"].lower() in texto:
            return p
    return None

def buscar_producto_por_categoria(texto):
    categorias = list({p["categoria"] for p in PRODUCTS})
    categoria_corregida = corregir_palabra(texto, categorias)
    return [p for p in PRODUCTS if p["categoria"] == categoria_corregida]

# --- Menú principal ---

MENU_PRINCIPAL = """
¿Qué andabas buscando?

1) Ver horarios
2) Ver sucursales
3) Ver categorías
4) Buscar un producto
5) Hablar con un asesor
"""

# --- Endpoint ---

@router.post("/")
async def chat(request: ChatRequest):
    user_message = request.message.lower().strip()
    user_id = request.user_id

    # Si el usuario no tiene estado → mostrar menú
    if user_id not in user_states:
        user_states[user_id] = "menu_principal"
        return {"type": "general", "data": MENU_PRINCIPAL}

    estado = user_states[user_id]

    # --- ESTADO: menú principal ---
    if estado == "menu_principal":
        if user_message == "1":
            return {"type": "general", "data": STORE_INFO["horarios"]}

        if user_message == "2":
            suc = "\n- ".join(STORE_INFO["sucursales"])
            return {"type": "general", "data": f"Nuestras sucursales:\n- {suc}"}

        if user_message == "3":
            categorias = sorted(list({p["categoria"] for p in PRODUCTS}))
            lista = "\n- ".join(categorias)
            return {"type": "general", "data": f"Categorías disponibles:\n- {lista}"}

        if user_message == "4":
            user_states[user_id] = "buscando_producto"
            return {"type": "general", "data": "Decime qué producto o categoría estás buscando."}

        if user_message == "5":
            return {"type": "general", "data": "Podés comunicarte con un asesor al WhatsApp: +54 9 11 1234 5678"}

        # Si no elige una opción válida
        return {"type": "general", "data": "No entendí la opción. Elegí un número del 1 al 5."}

    # --- ESTADO: buscando producto ---
    if estado == "buscando_producto":
        # 1) Buscar por nombre exacto
        producto = buscar_producto_por_nombre(user_message)
        if producto:
            info = (
                f"{producto['nombre']}\n"
                f"Precio: ${producto['precio']}\n"
                f"Talles: {', '.join(producto['talles'])}\n"
                f"Stock: {producto['stock']} unidades"
            )
            return {"type": "general", "data": info}

        # 2) Buscar por categoría (con corrección de ortografía)
        productos_categoria = buscar_producto_por_categoria(user_message)
        if productos_categoria:
            lista = "\n".join([f"- {p['nombre']} (${p['precio']})" for p in productos_categoria])
            return {"type": "general", "data": f"Productos en esa categoría:\n{lista}"}

        # 3) Si no encuentra nada → IA
        fallback_prompt = f"""
        Sos LlaqtaBot, asistente de una tienda de ropa de campo argentina.
        Respondé SIEMPRE en texto plano.
        El usuario buscó un producto pero no encontramos coincidencias.
        Intentá ayudarlo sin inventar productos.
        Mensaje del usuario: "{user_message}"
        """

        llm_response = generate_llm_response(fallback_prompt)
        return {"type": "general", "data": llm_response}

    # --- Fallback general ---
    fallback_prompt = f"""
    Sos LlaqtaBot, asistente de una tienda de ropa de campo argentina.
    Respondé SIEMPRE en texto plano.
    Mensaje del usuario: "{user_message}"
    """

    llm_response = generate_llm_response(fallback_prompt)
    return {"type": "general", "data": llm_response}