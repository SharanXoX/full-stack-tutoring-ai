import React, { useState } from "react";
import LoadingSpinner from "./LoadingSpinner";

export default function FileUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function handleFileChange(e) {
    setFile(e.target.files[0]);
    setError(null);
  }

  async function handleUpload() {
    if (!file) {
      setError("Please select a file to upload.");
      return;
    }
    console.log("🚀 Starting upload for file:", file.name);
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      // Hardcoded user_id for demo purposes as per previous context
      formData.append("user_id", "student_demo"); 
      formData.append("user_role", "student");

      console.log("📤 Sending upload request to backend...");
      const res = await fetch("http://127.0.0.1:8000/api/content/upload", { 
        method: "POST",
        body: formData,
      });

      console.log("📬 Upload response status:", res.status);
      if (!res.ok) {
        const txt = await res.text();
        console.error("❌ Upload failed:", txt);
        throw new Error(txt || `Upload failed: ${res.status}`);
      }

      const data = await res.json();
      console.log("✅ Upload successful! Response data:", data);
      // Example returned data: { file_id: "...", title: "...", size: ... }
      if (onUploadSuccess) {
        console.log("📞 Calling onUploadSuccess callback with data...");
        onUploadSuccess(data);
      } else {
        console.warn("⚠️ No onUploadSuccess callback provided!");
      }
    } catch (err) {
      console.error("❌ Upload error:", err);
      setError(err.message || "Upload failed");
    } finally {
      setLoading(false);
      console.log("🏁 Upload process completed");
    }
  }

  return (
    <>
      {loading && <LoadingSpinner message="📤 Uploading your document..." />}
      
      <div className="p-2">
        <input type="file" onChange={handleFileChange} className="mb-2" />
        <div>
          <button
            onClick={handleUpload}
            disabled={loading}
            className="px-4 py-2 rounded bg-indigo-600 text-white disabled:opacity-50"
          >
            {loading ? "Uploading..." : "Upload"}
          </button>
        </div>
        {error && <p className="text-red-500 mt-2">{error}</p>}
      </div>
    </>
  );
}
