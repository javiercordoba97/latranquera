import re

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

def interpretar_opcion_menu(user_message: str) -> str | None:
    """Mapea texto natural o números a opciones '1'–'5'."""
    m = user_message.lower().strip()
    m = re.sub(r"^[\s\-\•]+", "", m)

    if m in ("1", "2", "3", "4", "5"):
        return m

    mo = re.match(r"^(opción|opcion|op)\s*([1-5])\b", m)
    if mo:
        return mo.group(2)

    mo = re.match(r"^([1-5])\s*[\).\]]", m)
    if mo:
        return mo.group(1)

    # Prioridad: contacto antes que palabras genéricas
    if any(
        k in m
        for k in (
            "whatsapp",
            "asesor",
            "humano",
            "persona",
            "teléfono",
            "telefono",
            "llamar",
            "contacto",
        )
    ):
        return "5"
    if any(
        k in m
        for k in (
            "horario",
            "horarios",
            "abierto",
            "cierra",
            "cerrado",
            "atención",
            "atencion",
            "abren",
            "cierran",
        )
    ):
        return "1"
    if any(
        k in m
        for k in (
            "sucursal",
            "sucursales",
            "dónde",
            "donde",
            "ubicación",
            "ubicacion",
            "dirección",
            "direccion",
            "local",
            "tienda física",
            "tienda fisica",
        )
    ):
        return "2"
    if any(
        k in m
        for k in (
            "categoría",
            "categorías",
            "categoria",
            "categorias",
            "qué venden",
            "que venden",
            "rubros",
        )
    ):
        return "3"
    # No incluir "tienen"/"tienes"/"tenés" acá: suelen ir con una pregunta de producto
    # ("¿tienen ponchos?") y deben resolverse por catálogo o por el LLM, no por el ítem 4.
    if any(
        k in m
        for k in (
            "buscar",
            "producto",
            "productos",
            "precio",
            "catálogo",
            "catalogo",
            "comprar",
            "stock",
        )
    ):
        return "4"

    return None


def es_saludo_o_mensaje_corto(user_message: str) -> bool:
    m = user_message.lower().strip()
    if len(m) > 50:
        return False
    saludos = (
        "hola",
        "buenas",
        "buen día",
        "buenos días",
        "buenas tardes",
        "buenas noches",
        "qué tal",
        "que tal",
        "hey",
        "buen dia",
    )
    return any(s in m for s in saludos) or m in ("ok", "gracias", "dale")


def corregir_palabra(palabra, opciones):
    match = get_close_matches(palabra.lower(), opciones, n=1, cutoff=0.6)
    return match[0] if match else palabra

def _normalizar_consulta_producto(texto: str) -> str:
    """Quita muletillas típicas de preguntas para matchear categorías y nombres."""
    m = texto.lower()
    for noise in (
        "¿",
        "?",
        "¡",
        "!",
        ",",
        ".",
    ):
        m = m.replace(noise, " ")
    palabras_ruido = (
        "tienen",
        "tienes",
        "tenés",
        "tenes",
        "hay",
        "venden",
        "vendes",
        "busco",
        "quiero",
        "necesito",
        "algún",
        "alguna",
        "algun",
        "disponible",
        "disponibles",
        "con",
        "stock",
        "de",
        "para",
        "un",
        "una",
        "unos",
        "unas",
        "el",
        "la",
        "los",
        "las",
    )
    for w in palabras_ruido:
        m = re.sub(rf"\b{re.escape(w)}\b", " ", m)
    m = re.sub(r"\s+", " ", m).strip()
    return m


def buscar_producto_por_nombre(texto):
    texto_l = texto.lower()
    nucleo = _normalizar_consulta_producto(texto)
    for p in PRODUCTS:
        nombre = p["nombre"].lower()
        if nombre in texto_l:
            return p
        if nucleo and nombre in nucleo:
            return p
        for palabra in nombre.split():
            if len(palabra) >= 4 and palabra in texto_l:
                return p
    if nucleo:
        for p in PRODUCTS:
            for palabra in nucleo.split():
                if len(palabra) >= 3 and palabra in p["nombre"].lower():
                    return p
    return None


def buscar_producto_por_categoria(texto):
    categorias = sorted({p["categoria"] for p in PRODUCTS})
    texto_l = texto.lower()
    nucleo = _normalizar_consulta_producto(texto)

    for cat in categorias:
        if cat in texto_l or cat in nucleo:
            return [p for p in PRODUCTS if p["categoria"] == cat]
        if cat.endswith("s") and len(cat) > 3:
            singular = cat[:-1]
            if singular in texto_l or singular in nucleo:
                return [p for p in PRODUCTS if p["categoria"] == cat]

    for muestra in (nucleo, texto_l):
        if not muestra.strip():
            continue
        categoria_corregida = corregir_palabra(muestra, categorias)
        if categoria_corregida in categorias:
            return [p for p in PRODUCTS if p["categoria"] == categoria_corregida]
        for palabra in muestra.split():
            if len(palabra) < 3:
                continue
            matches = get_close_matches(palabra, categorias, n=1, cutoff=0.65)
            if matches:
                c = matches[0]
                return [p for p in PRODUCTS if p["categoria"] == c]

    return []

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
    raw_message = request.message.strip()
    user_message = raw_message.lower().strip()
    user_id = request.user_id

    if user_id not in user_states:
        user_states[user_id] = "menu_principal"

    estado = user_states[user_id]

    # --- ESTADO: menú principal ---
    if estado == "menu_principal":
        # 1) Catálogo primero: preguntas tipo "¿tienen ponchos?" deben ir acá, no al ítem 4 del menú
        producto = buscar_producto_por_nombre(user_message)
        if producto:
            user_states[user_id] = "buscando_producto"
            info = (
                f"{producto['nombre']}\n"
                f"Precio: ${producto['precio']}\n"
                f"Talles: {', '.join(producto['talles'])}\n"
                f"Stock: {producto['stock']} unidades"
            )
            return {"type": "general", "data": info}

        productos_categoria = buscar_producto_por_categoria(user_message)
        if productos_categoria:
            user_states[user_id] = "buscando_producto"
            lista = "\n".join(
                [f"- {p['nombre']} (${p['precio']})" for p in productos_categoria]
            )
            return {
                "type": "general",
                "data": f"Sí, tenemos en esa línea. Algunos productos:\n{lista}",
            }

        opcion = interpretar_opcion_menu(user_message)

        if opcion is None and es_saludo_o_mensaje_corto(user_message):
            return {
                "type": "general",
                "data": f"{MENU_PRINCIPAL}\n\nPodés elegir el número o escribir por ejemplo \"horarios\", \"sucursales\" o \"buscar producto\".",
            }

        if opcion is None:
            llm_prompt = f"""Sos el asistente de La Tranquera (tienda argentina: indumentaria y artículos de campo).

Datos reales (usá solo esto para horarios, envíos y locales; no inventes otros):
- Horarios: {STORE_INFO["horarios"]}
- Envíos: {STORE_INFO["envios"]}
- Devoluciones: {STORE_INFO["devoluciones"]}
- Sucursales: {", ".join(STORE_INFO["sucursales"])}
- Categorías de producto que manejamos: {", ".join(sorted({p['categoria'] for p in PRODUCTS}))}

El usuario escribió: "{raw_message}"

Respondé en español rioplatense, breve y claro, texto plano sin markdown.
Si la pregunta es sobre productos, orientá nombrando categorías reales del listado y decí que puede pedir precios o stock eligiendo en el menú la opción de buscar producto o escribiendo el nombre de la categoría.
No inventes precios ni nombres de productos concretos."""

            llm_response = await generate_llm_response(llm_prompt)
            return {"type": "general", "data": llm_response}

        if opcion == "1":
            return {"type": "general", "data": STORE_INFO["horarios"]}

        if opcion == "2":
            suc = "\n- ".join(STORE_INFO["sucursales"])
            return {"type": "general", "data": f"Nuestras sucursales:\n- {suc}"}

        if opcion == "3":
            categorias = sorted(list({p["categoria"] for p in PRODUCTS}))
            lista = "\n- ".join(categorias)
            return {"type": "general", "data": f"Categorías disponibles:\n- {lista}"}

        if opcion == "4":
            user_states[user_id] = "buscando_producto"
            return {
                "type": "general",
                "data": "Decime qué producto o categoría estás buscando (podés escribir por ejemplo mates, ponchos, sombreros).",
            }

        if opcion == "5":
            return {"type": "general", "data": "Podés comunicarte con un asesor al WhatsApp: +54 9 11 1234 5678"}

    # --- ESTADO: buscando producto ---
    if estado == "buscando_producto":
        if any(
            k in user_message
            for k in (
                "menú",
                "menu",
                "volver",
                "inicio",
                "opciones",
                "principal",
            )
        ):
            user_states[user_id] = "menu_principal"
            return {"type": "general", "data": MENU_PRINCIPAL}

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
        Sos el asistente de La Tranquera (indumentaria y artículos de campo argentinos).
        Respondé SIEMPRE en texto plano.
        El usuario buscó un producto pero no encontramos coincidencias en el catálogo.
        Intentá orientarlo sin inventar productos ni precios.
        Mensaje del usuario: "{raw_message}"
        """

        llm_response = await generate_llm_response(fallback_prompt)
        return {"type": "general", "data": llm_response}

    # --- Fallback general (no debería ocurrir con los estados actuales) ---
    fallback_prompt = f"""
    Sos el asistente de La Tranquera (indumentaria y artículos de campo argentinos).
    Respondé SIEMPRE en texto plano.
    Mensaje del usuario: "{raw_message}"
    """

    llm_response = await generate_llm_response(fallback_prompt)
    return {"type": "general", "data": llm_response}