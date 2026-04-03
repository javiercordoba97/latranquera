// En Vercel: Settings → Environment Variables → VITE_API_URL = https://tu-backend.onrender.com
const API_URL = import.meta.env.VITE_API_URL || "https://latranquera.onrender.com";

const USER_ID_KEY = "llaqta_chat_user_id_v2";

let USER_ID = localStorage.getItem(USER_ID_KEY);
if (!USER_ID) {
  USER_ID = "user_" + Math.random().toString(36).substring(2, 10);
  localStorage.setItem(USER_ID_KEY, USER_ID);
}

/** Nueva sesión en el servidor (estado del chat reiniciado) y nuevo id local. */
export function newChatSession() {
  USER_ID = "user_" + Math.random().toString(36).substring(2, 10);
  localStorage.setItem(USER_ID_KEY, USER_ID);
  return USER_ID;
}

function normalizeBotPayload(body) {
  const data = body?.data;
  if (typeof data === "string") return data;
  if (data && typeof data === "object" && data.error) {
    return typeof data.error === "string" ? data.error : "Error del asistente.";
  }
  if (data != null) return String(data);
  return "No recibimos una respuesta válida.";
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
      cache: "no-store",
    });

    const body = await response.json().catch(() => ({}));

    if (!response.ok) {
      const detail = Array.isArray(body.detail)
        ? body.detail.map((d) => d.msg || d).join(" ")
        : body.detail;
      return {
        type: "general",
        data: detail || "El servidor respondió con un error. Intentá de nuevo.",
        ok: false,
      };
    }

    return { ...body, data: normalizeBotPayload(body), ok: true };
  } catch (error) {
    return {
      type: "general",
      data: "Hubo un problema de conexión. Intentá de nuevo.",
      ok: false,
    };
  }
}
