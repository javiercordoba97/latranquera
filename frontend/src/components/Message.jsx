export default function Message({ from, text }) {
  return (
    <div className={`message-wrapper ${from}`}>
      <div className="message-bubble">
        {text.split("\n").map((line, i) => (
          <p key={i}>{line}</p>
        ))}
      </div>
    </div>
  );
}