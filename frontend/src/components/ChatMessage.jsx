import ReactMarkdown from "react-markdown";

export default function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`message ${isUser ? "user" : "assistant"} ${message.error ? "error" : ""}`}>
      {!isUser && <div className="avatar">🎓</div>}
      <div className="bubble">
        {isUser ? (
          message.content
        ) : (
          <ReactMarkdown>{message.content}</ReactMarkdown>
        )}
      </div>
      {isUser && <div className="avatar user-avatar">You</div>}
    </div>
  );
}
