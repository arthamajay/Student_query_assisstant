import { useState, useRef, useEffect } from "react";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import "./App.css";

const WELCOME_MESSAGE = {
  id: 0,
  role: "assistant",
  content:
    "Hi! I'm the CVR College assistant 🎓 Ask me anything about courses, faculty, placements, infrastructure, or admissions.",
};

function App() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text) => {
    const userMsg = { id: Date.now(), role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!res.ok) throw new Error("Server error");

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, role: "assistant", content: data.answer },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <span className="logo-icon">🎓</span>
          <span className="logo-text">CVR Assistant</span>
        </div>
        <div className="sidebar-divider" />
        <p className="sidebar-hint">Ask me about:</p>
        <ul className="sidebar-topics">
          <li>📚 Courses &amp; Programs</li>
          <li>👨‍🏫 Faculty &amp; Staff</li>
          <li>💼 Placements</li>
          <li>🏛️ Infrastructure</li>
          <li>📞 Contact &amp; Transport</li>
          <li>ℹ️ About CVR</li>
        </ul>
        <div className="sidebar-footer">Powered by LLaMA 3.3 + RAG</div>
      </aside>

      {/* Main chat area */}
      <main className="chat-area">
        <header className="chat-header">
          <h1>CVR College Chatbot</h1>
        </header>

        <div className="messages-container">
          {messages.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}
          {loading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>

        <ChatInput onSend={sendMessage} disabled={loading} />
      </main>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="message assistant">
      <div className="avatar">🎓</div>
      <div className="bubble typing">
        <span />
        <span />
        <span />
      </div>
    </div>
  );
}

export default App;
