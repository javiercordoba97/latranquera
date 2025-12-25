from fastapi import APIRouter
from pydantic import BaseModel
from app.data.store_data import PRODUCTS, STORE_INFO
from app.services.llm_service import generate_llm_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(request: ChatRequest):
    user_message = request.message.lower()

    # --- Respuestas directas sin LLM ---
    if "envio" in user_message or "envíos" in user_message:
        return {"type": "general", "data": STORE_INFO["envios"]}

    if "devolucion" in user_message or "devoluciones" in user_message:
        return {"type": "general", "data": STORE_INFO["devoluciones"]}

    if "sucursal" in user_message or "local" in user_message:
        return {
            "type": "general",
            "data": "Nuestras sucursales:\n- " + "\n- ".join(STORE_INFO["sucursales"])
        }

    if "horario" in user_message:
        return {"type": "general", "data": STORE_INFO["horarios"]}

    # --- Búsqueda de productos ---
    for p in PRODUCTS:
        if p["nombre"].lower() in user_message:
            info = (
                f"{p['nombre']}\n"
                f"Precio: ${p['precio']}\n"
                f"Talles disponibles: {', '.join(p['talles'])}\n"
                f"Stock: {p['stock']} unidades"
            )
            return {"type": "general", "data": info}

    # --- Si no entendemos, usamos el LLM ---
    fallback_prompt = f"""
    Sos LlaqtaBot, asistente de una tienda de ropa de campo argentina.
    Respondé SIEMPRE en texto plano, sin JSON.
    Si el usuario pregunta algo que no está en la base de datos, respondé de forma amable y breve.
    Mensaje del usuario: "{user_message}"
    """

    llm_response = generate_llm_response(fallback_prompt)

    return {"type": "general", "data": llm_response}