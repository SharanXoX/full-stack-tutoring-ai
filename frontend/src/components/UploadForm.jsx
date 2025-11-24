// src/components/UploadForm.jsx
import React, { useState } from "react";

export default function UploadForm(){
  const [file,setFile] = useState(null);
  const [teacherId,setTeacherId] = useState("teacher_demo");
  const [result,setResult] = useState(null);
  const [loading,setLoading] = useState(false);

  const handle = async (e) => {
    e.preventDefault();
    if(!file) return alert("Choose a file");
    setLoading(true);
    const form = new FormData();
    form.append("file", file);
    form.append("teacher_id", teacherId);

    try {
      const resp = await fetch("http://127.0.0.1:8000/api/content/upload", {
        method: "POST",
        body: form
      });
      const data = await resp.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handle}>
        <label>Teacher ID: <input value={teacherId} onChange={e=>setTeacherId(e.target.value)} /></label><br/>
        <input type="file" onChange={e=>setFile(e.target.files[0])} /><br/>
        <button type="submit" disabled={loading}>{loading ? "Uploading..." : "Upload"}</button>
      </form>
      {result && <pre style={{ marginTop: 12 }}>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
