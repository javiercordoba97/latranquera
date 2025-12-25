import { useState } from "react";
import ChatBox from "./ChatBox";

export default function ChatBubble() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <div className="chat-bubble" onClick={() => setOpen(!open)}>
        💬
      </div>

      {open && (
        <div className="chat-window">
          <ChatBox />
        </div>
      )}
    </>
  );
}