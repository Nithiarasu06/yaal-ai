import { useState } from "react";
import {
  Bot,
  Copy,
  Cpu,
  Eraser,
  MessageCircle,
  Send,
  Sparkles,
} from "lucide-react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

interface Message {
  role: "user" | "assistant";
  content: string;
  generationTime?: number;
  generatedTokens?: number;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [backendOnline, setBackendOnline] = useState(true);
  const [copied, setCopied] = useState<number | null>(null);

  const generateResponse = async () => {
    const trimmedPrompt = prompt.trim();

    if (!trimmedPrompt || loading) {
      return;
    }

    const userMessage: Message = {
      role: "user",
      content: trimmedPrompt,
    };

    setMessages((previous) => [...previous, userMessage]);
    setPrompt("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          prompt: trimmedPrompt,
          max_new_tokens: 150,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: "assistant",
        content: data.response || "பதில் கிடைக்கவில்லை.",
        generationTime: data.generation_time,
        generatedTokens: data.generated_tokens,
      };

      setMessages((previous) => [...previous, assistantMessage]);
      setBackendOnline(true);
    } catch (error) {
      console.error("Backend error:", error);

      setBackendOnline(false);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "மன்னிக்கவும். YAAL backend-ஐ இணைக்க முடியவில்லை. Python backend இயங்குகிறதா என்பதை சரிபார்க்கவும்.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    generateResponse();
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>,
  ) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      generateResponse();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const copyResponse = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(index);

      setTimeout(() => {
        setCopied(null);
      }, 1500);
    } catch (error) {
      console.error("Copy failed:", error);
    }
  };

  return (
    <div className="app-shell">
      <div className="background-grid" />
      <div className="background-glow glow-one" />
      <div className="background-glow glow-two" />

      <header className="topbar">
        <div className="brand">
          <div className="yaal-logo">
            <span>யாழ்</span>
            <div className="logo-pulse" />
          </div>

          <div className="brand-text">
            <h1>YAAL</h1>
            <span>தமிழுக்காக உருவாக்கப்பட்ட நுண்ணறிவு</span>
          </div>
        </div>

        <div className="topbar-right">
          <div className="engine-status">
            <span
              className={`status-dot ${
                backendOnline ? "online" : "offline"
              }`}
            />

            <span>
              {backendOnline ? "YAAL ENGINE ONLINE" : "ENGINE OFFLINE"}
            </span>
          </div>

          <button
            className="clear-button"
            onClick={clearChat}
            disabled={messages.length === 0}
            title="Clear conversation"
          >
            <Eraser size={16} />
            <span>Clear</span>
          </button>
        </div>
      </header>

      <main className="main-content">
        <section className="hero-section">
          <div className="hero-badge">
            <Sparkles size={14} />
            <span>TAMIL INTELLIGENCE</span>
          </div>

          <h2>
          தமிழில் கேளுங்கள்.
          <br />
          <span>YAAL உடன் உரையாடுங்கள்.</span>
        </h2>

          <p>
            தமிழில் கேள்விகளைக் கேளுங்கள். YAAL உங்கள் கேள்விகளுக்கு
            தமிழில் பதிலளிக்கிறது.
          </p>
        </section>

        <section className="engine-card">
          <div className="engine-card-left">
            <div className="engine-icon">
              <Cpu size={21} />
            </div>

            <div>
              <div className="engine-title">YAAL ENGINE</div>
              <div className="engine-subtitle">
                Sarvam-1 + Tamil LoRA
              </div>
            </div>
          </div>

          <div className="engine-metrics">
            <div className="metric">
              <span>MODEL</span>
              <strong>SARVAM-1</strong>
            </div>

            <div className="metric-divider" />

            <div className="metric">
              <span>ADAPTER</span>
              <strong>TAMIL LoRA</strong>
            </div>

            <div className="metric-divider" />

            <div className="metric">
              <span>GPU</span>
              <strong>RTX 3050</strong>
            </div>
          </div>

          <div className="engine-live">
            <span className="live-ring">
              <span />
            </span>
            <span>CUDA</span>
          </div>
        </section>

        <section
          className={`chat-container ${
            messages.length === 0 ? "empty-chat" : ""
          }`}
        >
          {messages.length === 0 ? (
            <div className="welcome-panel">
              <div className="welcome-orb">
                <div className="orb-core">
                  <Bot size={34} />
                </div>
              </div>

              <h3>வணக்கம்! நான் YAAL.</h3>

              <p>
                தமிழில் எதையும் கேளுங்கள்.
                <br />
                உங்கள் கேள்வியிலிருந்து தொடங்கலாம்.
              </p>

              <div className="suggestions">
                <button
                  onClick={() =>
                    setPrompt("தமிழ்நாட்டின் தலைநகரம் எது?")
                  }
                >
                  தமிழ்நாட்டின் தலைநகரம் எது?
                </button>

                <button
                  onClick={() =>
                    setPrompt(
                      "தமிழ்நாட்டின் விவசாயிகளுக்கு அரசு வழங்கும் உதவிகள் என்ன?",
                    )
                  }
                >
                  விவசாயிகளுக்கான அரசு உதவிகள் என்ன?
                </button>

                <button
                  onClick={() =>
                    setPrompt(
                      "தமிழில் செயற்கை நுண்ணறிவு என்றால் என்ன?",
                    )
                  }
                >
                  செயற்கை நுண்ணறிவு என்றால் என்ன?
                </button>
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message, index) => (
                <div
                  key={`${message.role}-${index}`}
                  className={`message-row ${message.role}`}
                >
                  <div className="message-avatar">
                    {message.role === "user" ? (
                      <MessageCircle size={17} />
                    ) : (
                      <span>யா</span>
                    )}
                  </div>

                  <div className="message-content">
                    <div className="message-name">
                      {message.role === "user" ? "YOU" : "YAAL"}
                    </div>

                    <div className="message-bubble">
                      <p>{message.content}</p>
                    </div>

                    {message.role === "assistant" && (
                      <div className="response-meta">
                        {message.generationTime !== undefined && (
                          <span>
                            <span className="yaal-mark">யாழ்</span>
                            {Number(message.generationTime).toFixed(2)}s
                          </span>
                        )}

                        {message.generatedTokens !== undefined && (
                          <span>
                            {message.generatedTokens} tokens
                          </span>
                        )}

                        <button
                          onClick={() =>
                            copyResponse(message.content, index)
                          }
                        >
                          <Copy size={12} />
                          {copied === index ? "Copied" : "Copy"}
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row assistant">
                  <div className="message-avatar">
                    <span>யாழ்</span>
                  </div>

                  <div className="message-content">
                    <div className="message-name">YAAL</div>

                    <div className="message-bubble typing-bubble">
                      <span />
                      <span />
                      <span />
                    </div>

                    <div className="generating-text">
                      YAAL is thinking...
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        <section className="composer-section">
          <form className="composer" onSubmit={handleSubmit}>
            <div className="composer-icon">
              <MessageCircle size={20} />
            </div>

            <textarea
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="தமிழில் கேளுங்கள்..."
              rows={1}
              disabled={loading}
            />

            <button
              type="submit"
              className="send-button"
              disabled={!prompt.trim() || loading}
              title="Send"
            >
              <Send size={19} />
            </button>
          </form>

          <div className="composer-footer">
            <span>Shift + Enter for new line</span>

            <span className="footer-brand">
              YAAL <span>•</span> Sarvam-1 <span>•</span> Tamil LoRA
            </span>
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <span>YAAL</span>
        <span>தமிழ் நுண்ணறிவு</span>
        <span>•</span>
        <span>Local GPU Inference</span>
      </footer>
    </div>
  );
}

export default App;