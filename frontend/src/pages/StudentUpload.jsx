import React, { useState, useEffect, useRef } from "react";
import FileUpload from "../components/FileUpload";
import LoadingSpinner from "../components/LoadingSpinner";
import { useAppContext } from "../context/AppContext";
import { useNavigate } from "react-router-dom";

function SummarySection() {
  const { summary } = useAppContext();
  if (!summary) return null;
  
  const topic = summary.topic || "Document Summary";
  const paragraphs = summary.summary_paragraphs || [];
  const keyPoints = summary.key_points || [];

  // Fallback for older format if backend returns simple string 'summary'
  const fallbackSummary = summary.summary; 

  return (
    <div className="mt-8 bg-white shadow-xl p-8 rounded-2xl border border-gray-100">
      <h2 className="text-3xl font-extrabold text-indigo-800 mb-6 border-b pb-4">
        📚 {topic}
      </h2>
      
      {/* Summary Section */}
      <div className="mb-8 space-y-4 text-gray-800 leading-relaxed text-lg">
        {paragraphs.length > 0 ? (
          paragraphs.map((para, idx) => (
            <p 
              key={idx} 
              dangerouslySetInnerHTML={{ __html: para }} 
              className="text-justify"
            />
          ))
        ) : (
           /* Fallback if no paragraphs array */
           <p className="whitespace-pre-wrap">{fallbackSummary}</p>
        )}
      </div>
      
      {/* Key Points Section */}
      {keyPoints.length > 0 && (
        <div className="mt-8 bg-indigo-50 p-6 rounded-xl border border-indigo-100">
          <h3 className="text-xl font-bold text-indigo-900 mb-4 flex items-center">
            <span className="bg-indigo-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-3 text-sm">🔑</span>
            Key Takeaways
          </h3>
          <div className="grid grid-cols-1 gap-4">
            {keyPoints.map((kp, i) => {
              // Handle both object {term, explanation} and string formats
              if (typeof kp === 'object' && kp.term) {
                return (
                  <div key={i} className="bg-white p-4 rounded-lg shadow-sm border-l-4 border-indigo-500">
                     <span className="font-bold text-indigo-800 text-lg mr-2">{kp.term}:</span>
                     <span 
                       className="text-gray-800 text-md leading-relaxed"
                       dangerouslySetInnerHTML={{ __html: kp.explanation }}
                     />
                  </div>
                );
              } else {
                 // Fallback for string list
                 return (
                  <div key={i} className="flex items-start bg-white p-4 rounded-lg shadow-sm">
                    <span className="text-indigo-600 mr-2 mt-1">•</span>
                    <span className="text-gray-800 text-md">{kp}</span>
                  </div>
                 );
              }
            })}
          </div>
        </div>
      )}
    </div>
  );
}

export default function StudentUpload() {
  const { setUploadedFile, setSummary, setTopic } = useAppContext();
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [timer, setTimer] = useState(60);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const timerRef = useRef(null);

  useEffect(() => {
    if (loadingSummary) {
      setTimer(60);
      timerRef.current = setInterval(() => {
        setTimer((prev) => (prev > 0 ? prev - 1 : 0));
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [loadingSummary]);

  const handleUploadSuccess = async (fileMeta) => {
    console.log("📤 Upload success! File metadata:", fileMeta);
    setUploadedFile(fileMeta);
    setError(null);
    setLoadingSummary(true);
    setSummary(null); 
    
    try {
      console.log("📡 Calling summarize endpoint with file_id:", fileMeta.file_id);
      const res = await fetch("http://127.0.0.1:8000/api/content/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          file_id: fileMeta.file_id,
          max_length: 500 
        }),
      });
      
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || `Summarize failed: ${res.status}`);
      }
      const data = await res.json(); 
      console.log("✅ Summary data received", data);
      setSummary(data);
      if (data.topic) setTopic(data.topic);
    } catch (err) {
      console.error("❌ Summarize error", err);
      if (err.message && (err.message.includes("413") || err.message.includes("rate_limit"))) {
        setError("Document processing limit reached. Please wait 60 seconds and try again.");
      } else {
        setError(err.message || "Failed to summarize");
      }
    } finally {
      setLoadingSummary(false);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto min-h-screen bg-gray-50">
      {loadingSummary && (
        <LoadingSpinner 
          message={`🤖 Antigravity is analyzing your document... This deep analysis may take up to ${timer} seconds.`} 
        />
      )}
      
      <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold text-gray-800">Upload Document</h2>
          <button
          onClick={() => navigate("/exam-prep", { state: { autoStart: true } })}
          className="px-6 py-3 bg-green-600 text-white font-medium rounded-lg shadow-lg hover:bg-green-700 transition transform hover:-translate-y-1"
        >
          Take Quiz Now
        </button>
      </div>

      <div className="mb-10 p-8 bg-white rounded-2xl shadow-sm border border-gray-100">
        <FileUpload onUploadSuccess={handleUploadSuccess} />
        {error && <div className="mt-4 p-4 text-red-700 bg-red-50 rounded border border-red-200">{error}</div>}
      </div>

      <SummarySection />
    </div>
  );
}
