import { useState, useEffect } from "react";
import { sendMessage } from "../services/api";
import Message from "./Message";
import InputBox from "./InputBox";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);

  // Saludo inicial del bot
  useEffect(() => {
    setMessages([
      { from: "bot", text: "Hola, soy LlaqtaBot ¿en qué te puedo ayudar?" }
    ]);
  }, []);

  const handleSend = async (text) => {
    // Mostrar mensaje del usuario
    setMessages((prev) => [...prev, { from: "user", text }]);

    // Llamar al backend
    const response = await sendMessage(text);

    let botText = "";

    if (response.type === "nutrition") {
      botText = JSON.stringify(response.data, null, 2);
    } else if (response.type === "general") {
      botText = response.data;
    } else {
      botText = "Hubo un error interpretando la respuesta del modelo.";
    }

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