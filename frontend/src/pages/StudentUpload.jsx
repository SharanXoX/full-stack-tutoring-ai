import React, { useState } from "react";
import FileUpload from "../components/FileUpload";
import LoadingSpinner from "../components/LoadingSpinner";
import { useAppContext } from "../context/AppContext";
import { useNavigate } from "react-router-dom";

function SummarySection() {
  const { summary } = useAppContext();
  if (!summary) return null;
  
  const topic = summary.topic || "Document Summary";
  
  return (
    <div className="mt-6 bg-white shadow-lg p-6 rounded-lg border border-gray-200">
      <h2 className="text-2xl font-bold text-indigo-700 mb-4">
        📚 Document Summary: {topic}
      </h2>
      
      <div className="mb-6 max-h-96 overflow-y-auto pr-2 custom-scrollbar">
        <p className="text-gray-800 leading-relaxed text-justify whitespace-pre-wrap">
          {summary.summary}
        </p>
      </div>
      
      {summary.key_points && summary.key_points.length > 0 && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">Core Concepts</h3>
          <ul className="space-y-2">
            {summary.key_points.map((kp, i) => (
              <li key={i} className="flex items-start">
                <span className="text-indigo-600 mr-2">•</span>
                <span className="text-gray-700">{kp}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default function StudentUpload() {
  const { setUploadedFile, setSummary, setTopic } = useAppContext();
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleUploadSuccess = async (fileMeta) => {
    console.log("📤 Upload success! File metadata:", fileMeta);
    setUploadedFile(fileMeta);
    setError(null);
    setLoadingSummary(true);
    console.log("🔄 Loading spinner activated");
    try {
      console.log("📡 Calling summarize endpoint with file_id:", fileMeta.file_id);
      const res = await fetch("http://127.0.0.1:8000/api/content/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          file_id: fileMeta.file_id,
          max_length: 500  // Request longer, more detailed summary
        }),
      });
      console.log("📬 Summarize response status:", res.status);
      if (!res.ok) {
        const txt = await res.text();
        console.error("❌ Summarize failed:", txt);
        throw new Error(txt || `Summarize failed: ${res.status}`);
      }
      const data = await res.json(); // expected: { summary, key_points }
      console.log("✅ Summary data received:", data);
      setSummary(data);
      // Auto topic heuristics: first key point, or file title, or fallback
      const autoTopic = data.key_points?.[0] || fileMeta.original_filename || "Generated Topic";
      console.log("📝 Auto-extracted topic:", autoTopic);
      setTopic(autoTopic);
    } catch (err) {
      console.error("❌ Summarize error", err);
      setError(err.message || "Failed to summarize");
    } finally {
      setLoadingSummary(false);
      console.log("🔄 Loading spinner deactivated");
    }
  };

  return (
    <div className="p-6">
      {loadingSummary && <LoadingSpinner message="🤖 Antigravity is analyzing your document & generating summary..." />}
      
      <h2 className="text-xl font-semibold mb-4">Upload Document</h2>
      <FileUpload onUploadSuccess={handleUploadSuccess} />
      {error && <p className="text-red-500 mt-2">{error}</p>}
      <SummarySection />
      <div className="mt-4">
        <button
          onClick={() => navigate("/exam-prep")}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          Take Quiz
        </button>
      </div>
    </div>
  );
}
