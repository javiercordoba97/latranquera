import { useState, useEffect } from "react";
import { sendMessage, newChatSession } from "../services/api";
import Message from "./Message";
import InputBox from "./InputBox";

const SALUDO_INICIAL =
  "Hola, bienvenido a La Tranquera. ¿En qué te puedo ayudar?";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setMessages([{ from: "bot", text: SALUDO_INICIAL }]);
  }, []);

  const handleNuevaConversacion = () => {
    newChatSession();
    setMessages([{ from: "bot", text: SALUDO_INICIAL }]);
  };

  const handleSend = async (text) => {
    setMessages((prev) => [...prev, { from: "user", text }]);
    setIsLoading(true);

    try {
      const response = await sendMessage(text);
      const botText =
        response.data ||
        "Hubo un error interpretando la respuesta del servidor.";
      setMessages((prev) => [...prev, { from: "bot", text: botText }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbox-content">
      <div className="chatbox-header">
        <span className="chatbox-title">Asistente</span>
        <button
          type="button"
          className="chatbox-reset"
          onClick={handleNuevaConversacion}
        >
          Nueva conversación
        </button>
      </div>
      <div className="chatbox-messages">
        {messages.map((msg, i) => (
          <Message key={i} from={msg.from} text={msg.text} />
        ))}
        {isLoading ? (
          <Message from="bot" text="Escribiendo…" />
        ) : null}
      </div>

      <InputBox onSend={handleSend} disabled={isLoading} />
    </div>
  );
}