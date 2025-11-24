import React, { useState, useEffect } from 'react';

function HomeworkHelp() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [hints, setHints] = useState([]);
  const [solution, setSolution] = useState(null);
  const [currentHintIndex, setCurrentHintIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const userId = "student_demo";

  // Fetch homework history on load
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/homework/history?user_id=${userId}`)
      .then(res => res.json())
      .then(data => setHistory(data))
      .catch(err => console.error("Failed to load history:", err));
  }, []);

  const handleSendMessage = async () => {
    if (!inputText.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: inputText,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/homework/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, problem: inputText }),
      });

      const data = await response.json();
      setSessionId(data.session_id);
      setHints(data.hints || []);
      setSolution(data.solution);
      setCurrentHintIndex(0);

      // Add AI response
      const aiMessage = {
        role: 'ai',
        content: `I can help you with that! I've prepared ${data.hints?.length || 0} hints to guide you through this problem.`,
        hints: data.hints,
        solution: data.solution,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error solving problem:", error);
      const errorMessage = {
        role: 'ai',
        content: "Sorry, I couldn't process that. Please try again.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const showNextHint = (messageHints) => {
    if (currentHintIndex < messageHints.length) {
      const hintMessage = {
        role: 'ai',
        content: `💡 Hint ${currentHintIndex + 1}: ${messageHints[currentHintIndex]}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, hintMessage]);
      setCurrentHintIndex(currentHintIndex + 1);
    }
  };

  const showFullSolution = (messageSolution) => {
    const solutionMessage = {
      role: 'ai',
      content: `✅ Complete Solution:\n\n${messageSolution}`,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, solutionMessage]);
    setCurrentHintIndex(hints.length);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px', display: 'flex', gap: '20px', height: 'calc(100vh - 100px)' }}>
      {/* Main Chat Area */}
      <div style={{ flex: 2, display: 'flex', flexDirection: 'column', backgroundColor: 'white', borderRadius: '12px', border: '1px solid #dee2e6' }}>
        {/* Header */}
        <div style={{ padding: '20px', borderBottom: '2px solid #007bff', backgroundColor: '#f8f9fa', borderRadius: '12px 12px 0 0' }}>
          <h1 style={{ margin: 0, fontSize: '24px' }}>📚 Homework Help</h1>
          <p style={{ margin: '5px 0 0 0', color: '#666', fontSize: '14px' }}>
            Ask me any homework question and I'll guide you step-by-step!
          </p>
        </div>

        {/* Messages Area */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '20px',
          display: 'flex',
          flexDirection: 'column',
          gap: '15px'
        }}>
          {messages.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 20px', color: '#666' }}>
              <div style={{ fontSize: '64px', marginBottom: '20px' }}>💬</div>
              <h2 style={{ color: '#007bff' }}>Start a Conversation</h2>
              <p style={{ fontSize: '16px', marginTop: '10px' }}>
                Type your homework question below and I'll help you solve it!
              </p>
              <div style={{
                backgroundColor: '#f8f9fa',
                padding: '20px',
                borderRadius: '8px',
                marginTop: '30px',
                textAlign: 'left',
                maxWidth: '500px',
                margin: '30px auto 0'
              }}>
                <h3 style={{ marginTop: 0, fontSize: '16px' }}>💡 Example Questions:</h3>
                <ul style={{ fontSize: '14px', lineHeight: '2' }}>
                  <li>"Solve for x: 2x + 5 = 15"</li>
                  <li>"Explain photosynthesis"</li>
                  <li>"How do I factor x² - 5x + 6?"</li>
                  <li>"What is the Pythagorean theorem?"</li>
                </ul>
              </div>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div key={index} style={{
                display: 'flex',
                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
              }}>
                <div style={{
                  maxWidth: '70%',
                  padding: '12px 16px',
                  borderRadius: '12px',
                  backgroundColor: msg.role === 'user' ? '#007bff' : '#f8f9fa',
                  color: msg.role === 'user' ? 'white' : '#333',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word'
                }}>
                  {msg.content}
                  
                  {/* Show hint and solution buttons for AI messages with hints */}
                  {msg.role === 'ai' && msg.hints && msg.hints.length > 0 && (
                    <div style={{ marginTop: '15px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                      {currentHintIndex < msg.hints.length && (
                        <button
                          onClick={() => showNextHint(msg.hints)}
                          style={{
                            padding: '8px 16px',
                            backgroundColor: '#ffc107',
                            color: '#000',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: 'bold'
                          }}
                        >
                          💡 Show Hint {currentHintIndex + 1}/{msg.hints.length}
                        </button>
                      )}
                      {msg.solution && (
                        <button
                          onClick={() => showFullSolution(msg.solution)}
                          style={{
                            padding: '8px 16px',
                            backgroundColor: '#28a745',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: 'pointer',
                            fontSize: '14px',
                            fontWeight: 'bold'
                          }}
                        >
                          ✅ Show Solution
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {loading && (
            <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
              <div style={{
                padding: '12px 16px',
                borderRadius: '12px',
                backgroundColor: '#f8f9fa',
                color: '#666'
              }}>
                <span>Thinking</span>
                <span className="dots">...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div style={{
          padding: '20px',
          borderTop: '1px solid #dee2e6',
          backgroundColor: '#f8f9fa',
          borderRadius: '0 0 12px 12px'
        }}>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-end' }}>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your homework question here... (Press Enter to send)"
              rows={2}
              style={{
                flex: 1,
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #ccc',
                fontSize: '16px',
                fontFamily: 'inherit',
                resize: 'none'
              }}
              disabled={loading}
            />
            <button
              onClick={handleSendMessage}
              disabled={loading || !inputText.trim()}
              style={{
                padding: '12px 24px',
                backgroundColor: loading || !inputText.trim() ? '#ccc' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontSize: '16px',
                cursor: loading || !inputText.trim() ? 'not-allowed' : 'pointer',
                fontWeight: 'bold',
                height: '48px'
              }}
            >
              {loading ? '...' : '📤 Send'}
            </button>
          </div>
        </div>
      </div>

      {/* History Sidebar */}
      <div style={{
        flex: 1,
        backgroundColor: '#f8f9fa',
        padding: '20px',
        borderRadius: '12px',
        border: '1px solid #dee2e6',
        maxHeight: '100%',
        overflowY: 'auto'
      }}>
        <h3 style={{ marginTop: 0 }}>📝 Recent Problems</h3>
        {history.length === 0 ? (
          <p style={{ color: '#666', fontSize: '14px' }}>No homework history yet.</p>
        ) : (
          history.map((item) => (
            <div
              key={item.id}
              style={{
                backgroundColor: 'white',
                padding: '12px',
                borderRadius: '8px',
                marginBottom: '10px',
                cursor: 'pointer',
                border: '1px solid #dee2e6',
                transition: 'all 0.2s'
              }}
              onClick={() => {
                setInputText(item.problem);
                setMessages([]);
                setSessionId(null);
                setHints([]);
                setSolution(null);
                setCurrentHintIndex(0);
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#e7f3ff';
                e.currentTarget.style.borderColor = '#007bff';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'white';
                e.currentTarget.style.borderColor = '#dee2e6';
              }}
            >
              <div style={{ fontSize: '14px', marginBottom: '5px', color: '#333', fontWeight: '500' }}>
                {item.problem.length > 60 ? item.problem.substring(0, 60) + '...' : item.problem}
              </div>
              <div style={{ fontSize: '12px', color: '#666' }}>
                💡 {item.hint_count} hints • {new Date(item.timestamp).toLocaleDateString()}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default HomeworkHelp;
