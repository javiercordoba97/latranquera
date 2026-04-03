import asyncio
import requests
from app.config import settings


def _llm_sync(user_message: str) -> str:
    if not settings.OPENROUTER_API_KEY:
        return "El asistente no está configurado (falta OPENROUTER_API_KEY en el servidor)."

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    system_prompt = """
    Sos el asistente oficial de La Tranquera, una tienda argentina de productos tradicionales:
    mates, bombillas, cuchillos, termos e indumentaria gaucha.

    Tu estilo es amable, claro y profesional.
    No inventes productos ni precios.
    Si el usuario pide algo que no existe, ofrecé alternativas reales.
    Respondé siempre en texto plano, sin JSON.
    """

    payload = {
        "model": settings.DEFAULT_LLM_MODEL,
        "max_tokens": 400,
        "temperature": 0.6,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    }

    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=(10, 45)
        )
    except requests.RequestException as e:
        return f"No pude contactar al servicio de respuestas. Intentá de nuevo en un momento. ({e!s})"

    if response.status_code != 200:
        return "Hubo un error al conectar con el modelo. Probá más tarde o elegí una opción del menú."

    try:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        return "No se pudo interpretar la respuesta del modelo."


async def generate_llm_response(user_message: str) -> str:
    """Evita bloquear el event loop de FastAPI durante la llamada a OpenRouter."""
    return await asyncio.to_thread(_llm_sync, user_message)