// src/pages/StudentView.jsx
import React, { useState, useEffect, useRef } from 'react';

function StudentView() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const userId = "student_demo"; // Hardcoded for demo

  // Fetch history on load
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/chat/history?user_id=${userId}`)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setMessages(data);
        }
      })
      .catch(err => console.error("Failed to load history:", err));
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message: userMsg.content }),
      });
      
      const data = await response.json();
      const aiMsg = { role: 'ai', content: data.answer, timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMsg = { role: 'ai', content: "Error: Could not reach the AI Tutor.", timestamp: new Date().toISOString() };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', height: '90vh', display: 'flex', flexDirection: 'column' }}>
      <h1>AI Tutor Chat</h1>
      
      {/* Chat Container */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto', 
        border: '1px solid #ccc', 
        borderRadius: '8px', 
        padding: '20px',
        marginBottom: '20px',
        backgroundColor: '#f9f9f9'
      }}>
        {messages.length === 0 && <p style={{ textAlign: 'center', color: '#888' }}>Start a conversation!</p>}
        
        {messages.map((msg, index) => (
          <div key={index} style={{ 
            display: 'flex', 
            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
            marginBottom: '15px'
          }}>
            <div style={{ 
              maxWidth: '70%', 
              padding: '12px 16px', 
              borderRadius: '12px',
              backgroundColor: msg.role === 'user' ? '#007bff' : '#e9ecef',
              color: msg.role === 'user' ? 'white' : 'black',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <div style={{ fontSize: '0.85em', marginBottom: '4px', opacity: 0.8 }}>
                {msg.role === 'user' ? 'You' : 'AI Tutor'}
              </div>
              <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ textAlign: 'left', color: '#888', fontStyle: 'italic' }}>AI is typing...</div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div style={{ display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a question about your documents..."
          style={{ flex: 1, padding: '12px', borderRadius: '4px', border: '1px solid #ccc' }}
          disabled={loading}
        />
        <button 
          onClick={handleSend} 
          disabled={loading}
          style={{ 
            padding: '12px 24px', 
            backgroundColor: loading ? '#ccc' : '#007bff', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            cursor: loading ? 'not-allowed' : 'pointer' 
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default StudentView;
