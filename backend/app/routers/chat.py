from fastapi import APIRouter
from pydantic import BaseModel
from difflib import get_close_matches

from app.data.store_data import PRODUCTS, STORE_INFO
from app.services.llm_service import generate_llm_response

router = APIRouter()

# Estado por usuario
user_states = {}
user_last_category = {}
user_last_product = {}

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

# ============================
# CATEGORÍAS (siempre en plural)
# ============================

CATEGORIA_KEYWORDS = {
    "ponchos": ["ponch", "poncho", "ponchos"],
    "bombachas": ["bombach", "bombacha", "bombachas"],
    "alpargatas": ["alpargat", "alpargata", "alpargatas"],
    "fajas": ["faj", "faja", "fajas"],
    "sombreros": ["sombr", "sombrer", "sombrero", "sombreros"],
    "camisas": ["camis", "camisa", "camisas"],
    "chalecos": ["chal", "chalec", "chaleco", "chalecos"],
    "cintos": ["cint", "cinto", "cintos"],
    "boinas": ["boin", "boina", "boinas"],
    "mates": ["mate", "mates"],
    "materas": ["mater", "matera", "materas"],
    "cuchillos": ["cuchill", "cuchillo", "cuchillos"]
}

# ============================
# DETECCIÓN DE CATEGORÍA FLEXIBLE
# ============================

def detectar_categoria_flexible(texto):
    texto = texto.lower()
    coincidencias = []

    # 1) Coincidencia por keywords
    for categoria, keywords in CATEGORIA_KEYWORDS.items():
        for kw in keywords:
            if kw in texto:
                coincidencias.append(categoria)
                break

    # 2) Si no encontró nada → intentar corrección ortográfica
    if not coincidencias:
        categorias = list(CATEGORIA_KEYWORDS.keys())
        corregida = get_close_matches(texto, categorias, n=1, cutoff=0.6)
        if corregida:
            return corregida[0]
        return None

    # 3) Si encontró una sola → devolver esa categoría exacta (plural)
    if len(coincidencias) == 1:
        return coincidencias[0]

    # 4) Si hay varias → ambigüedad → repreguntar
    return coincidencias

# ============================
# DETECCIÓN DE PRODUCTO
# ============================

def detectar_producto(texto):
    texto = texto.lower()
    for p in PRODUCTS:
        if p["nombre"].lower() in texto:
            return p
    return None

# ============================
# PRODUCTOS POR CATEGORÍA
# ============================

def productos_por_categoria(categoria):
    return [p for p in PRODUCTS if p["categoria"] == categoria and p["stock"] > 0]

# ============================
# MENÚ PRINCIPAL
# ============================

MENU_PRINCIPAL = """
¿Qué andabas buscando?

1) Ver horarios
2) Ver sucursales
3) Ver categorías
4) Buscar un producto
5) Hablar con un asesor
"""

# ============================
# ENDPOINT PRINCIPAL
# ============================

@router.post("/")
async def chat(request: ChatRequest):
    user_message = request.message.lower().strip()
    user_id = request.user_id

    if user_id not in user_states:
        user_states[user_id] = "conversacion_libre"

    estado = user_states[user_id]

    # ============================
    # ESTADO: conversación libre
    # ============================

    if estado == "conversacion_libre":

        # Detectar producto explícito
        producto = detectar_producto(user_message)
        if producto:
            user_last_product[user_id] = producto["nombre"]
            user_last_category[user_id] = producto["categoria"]

        # Detectar categoría flexible
        categoria_detectada = detectar_categoria_flexible(user_message)

        # Si devuelve lista → ambigüedad → repreguntar
        if isinstance(categoria_detectada, list):
            opciones = ", ".join(categoria_detectada)
            return {
                "type": "general",
                "data": f"No me quedó claro. ¿Te referías a {opciones}?"
            }

        # Si detectó categoría clara → actualizar memoria
        if isinstance(categoria_detectada, str):
            user_last_category[user_id] = categoria_detectada

        # Preguntas de stock
        if any(x in user_message for x in ["quedan", "stock", "cuales", "tienen", "disponible", "disponibles"]):

            # Si detectó categoría explícita
            if isinstance(categoria_detectada, str):
                productos = productos_por_categoria(categoria_detectada)
                if productos:
                    lista = "\n".join([f"• {p['nombre']} — ${p['precio']}" for p in productos])
                    return {"type": "general", "data": f"Ahora tenemos en stock:\n\n{lista}"}

            # Si no detectó categoría → usar memoria
            if user_id in user_last_category:
                categoria = user_last_category[user_id]
                productos = productos_por_categoria(categoria)
                if productos:
                    lista = "\n".join([f"• {p['nombre']} — ${p['precio']}" for p in productos])
                    return {"type": "general", "data": f"Ahora tenemos en stock:\n\n{lista}"}

            # Si no hay nada claro → repreguntar
            return {
                "type": "general",
                "data": "¿De qué categoría querés saber? Puedo ayudarte con sombreros, camisas, cintos y más."
            }

        # Preguntas normales → IA
        if len(user_message.split()) > 1:
            prompt = f"""
            Sos TranqueraBot, asistente de La Tranquera.
            Respondé SIEMPRE en texto plano.
            Mensaje del usuario: "{user_message}"
            """
            respuesta = generate_llm_response(prompt)
            return {"type": "general", "data": respuesta}

        # Mensaje corto → menú
        user_states[user_id] = "menu_principal"
        user_last_category.pop(user_id, None)
        user_last_product.pop(user_id, None)
        return {"type": "general", "data": MENU_PRINCIPAL}

    # ============================
    # ESTADO: menú principal
    # ============================

    if estado == "menu_principal":

        # Borrar memoria
        user_last_category.pop(user_id, None)
        user_last_product.pop(user_id, None)

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

        return {"type": "general", "data": "No entendí la opción. Elegí un número del 1 al 5."}

    # ============================
    # ESTADO: buscando producto
    # ============================

    if estado == "buscando_producto":

        producto = detectar_producto(user_message)
        if producto:
            info = (
                f"{producto['nombre']}\n"
                f"Precio: ${producto['precio']}\n"
                f"Talles: {', '.join(producto['talles'])}\n"
                f"Stock: {producto['stock']} unidades"
            )
            return {"type": "general", "data": info}

        categoria = detectar_categoria_flexible(user_message)

        if isinstance(categoria, list):
            opciones = ", ".join(categoria)
            return {"type": "general", "data": f"¿Te referías a {opciones}?"}

        if isinstance(categoria, str):
            productos = productos_por_categoria(categoria)
            lista = "\n".join([f"- {p['nombre']} (${p['precio']})" for p in productos])
            return {"type": "general", "data": f"Productos en esa categoría:\n{lista}"}

        prompt = f"""
        Sos TranqueraBot, asistente de La Tranquera.
        Respondé SIEMPRE en texto plano.
        El usuario buscó un producto pero no encontramos coincidencias.
        Intentá ayudarlo sin inventar productos.
        Mensaje del usuario: "{user_message}"
        """
        respuesta = generate_llm_response(prompt)
        return {"type": "general", "data": respuesta}

    # ============================
    # FALLBACK
    # ============================

    prompt = f"""
    Sos TranqueraBot, asistente de La Tranquera.
    Respondé SIEMPRE en texto plano.
    Mensaje del usuario: "{user_message}"
    """
    respuesta = generate_llm_response(prompt)
    return {"type": "general", "data": respuesta}