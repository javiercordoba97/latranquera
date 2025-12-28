def detect_intent(message: str) -> str:
    """
    Detecta la intención del usuario para La Tranquera.
    Puede ser: saludo, categoría, producto o general.
    """

    message = message.lower()

    # Saludos
    greetings = ["hola", "buenas", "qué tal", "como va", "buen día", "buenas tardes", "buenas noches"]
    if any(g in message for g in greetings):
        return "greeting"

    # Categorías de La Tranquera
    categories = {
        "mates": ["mate", "mates"],
        "bombillas": ["bombilla", "bombillas"],
        "cuchillos": ["cuchillo", "cuchillos", "facón", "facones"],
        "termos": ["termo", "termos"],
        "indumentaria": ["poncho", "boina", "indumentaria", "ropa"],
    }

    for category, keywords in categories.items():
        if any(k in message for k in keywords):
            return f"category:{category}"

    # Productos específicos
    product_keywords = ["criollo", "camionero", "imperial", "acero", "inoxidable", "grabado"]
    if any(p in message for p in product_keywords):
        return "product"

    # Si no coincide con nada → general
    return "general"