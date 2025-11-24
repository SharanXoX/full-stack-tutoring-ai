// src/pages/Login.jsx
import React, { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const handle = (e) => {
    e.preventDefault();
    alert("Auth not wired yet");
  };
  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handle}>
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} /><br/><br/>
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} /><br/><br/>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
