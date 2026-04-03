import { useState } from "react";

export default function InputBox({ onSend, disabled = false }) {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (disabled || !text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <form onSubmit={handleSubmit} className="input-box">
      <input
        type="text"
        placeholder="Escribe tu mensaje..."
        value={text}
        disabled={disabled}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            handleSubmit(e);
          }
        }}
      />
      <button type="submit" disabled={disabled}>
        Enviar
      </button>
    </form>
  );
}