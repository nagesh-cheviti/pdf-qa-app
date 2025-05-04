import React, { useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await axios.post("http://localhost:8000/upload", formData);
      setFilename(res.data.filename);
      toast.success("Upload successful!");
    } catch (err) {
      console.error("Upload error:", err);
      toast.error("Failed to upload PDF.");
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("filename", filename);
      formData.append("question", question);

      const res = await axios.post("http://localhost:8000/ask", formData);
      setChatHistory((prev) => [...prev, { question, answer: res.data.answer }]);
      setQuestion(""); // Clear input
      toast.success("Answer received!");
    } catch (err) {
      console.error("Ask error:", err);
      toast.error("Failed to fetch answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo-section">
          <img src="/AI Planet Logo.svg" alt="logo" className="logo-img" />
        </div>
        <div className="upload-section">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={handleUpload} disabled={!file} className="upload-btn">
            Upload PDF
          </button>
        </div>
      </header>

      <div className="chat-area">
        {chatHistory.map((chat, index) => (
          <React.Fragment key={index}>
            <div className="chat-bubble user-bubble">
              <div className="avatar user-avatar">N</div>
              <div className="message">{chat.question}</div>
            </div>
            <div className="chat-bubble ai-bubble">
              <div className="avatar ai-avatar">ai</div>
              <div className="message">{chat.answer}</div>
            </div>
          </React.Fragment>
        ))}
      </div>

      <footer className="app-footer">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Send a message..."
          className="input-box"
        />
        <button
          onClick={handleAsk}
          disabled={!filename || !question || loading}
          className={`send-btn ${(!filename || !question || loading) ? 'disabled' : ''}`}
        >
          {loading ? (
            <span className="loading-dots">...</span>
          ) : (
            <img src="/Vector.svg" alt="send" className="send-icon" />
          )}
        </button>
      </footer>

      <ToastContainer position="top-right" autoClose={3000} />
    </div>
  );
}

export default App;
