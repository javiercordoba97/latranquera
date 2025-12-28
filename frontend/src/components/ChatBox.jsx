import { useState, useEffect } from "react";
import { sendMessage } from "../services/api";
import Message from "./Message";
import InputBox from "./InputBox";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);

  // Saludo inicial del bot
  useEffect(() => {
    setMessages([
      { from: "bot", text: "Hola, soy el asistente de La Tranquera. ¿En qué te puedo ayudar?" }
    ]);
  }, []);

  const handleSend = async (text) => {
    // Mostrar mensaje del usuario
    setMessages((prev) => [...prev, { from: "user", text }]);

    // Llamar al backend
    const response = await sendMessage(text);

    let botText = "";

    // El backend siempre devuelve { type: "...", data: "..." }
    botText = response.data || "Hubo un error interpretando la respuesta del modelo.";

    // Mostrar mensaje del bot
    setMessages((prev) => [...prev, { from: "bot", text: botText }]);
  };

  return (
    <div className="chatbox-content">
      <div className="chatbox-messages">
        {messages.map((msg, i) => (
          <Message key={i} from={msg.from} text={msg.text} />
        ))}
      </div>

      <InputBox onSend={handleSend} />
    </div>
  );
}