const API_URL = "https://latranquera.onrender.com";

// Generamos un user_id único por sesión del navegador
let USER_ID = localStorage.getItem("llaqta_user_id");

if (!USER_ID) {
  USER_ID = "user_" + Math.random().toString(36).substring(2, 10);
  localStorage.setItem("llaqta_user_id", USER_ID);
}

export async function sendMessage(message) {
  try {
    const response = await fetch(`${API_URL}/chat/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        user_id: USER_ID,
      }),
    });

    return await response.json();
  } catch (error) {
    return {
      type: "general",
      data: "Hubo un problema de conexión. Intentá de nuevo.",
    };
  }
}