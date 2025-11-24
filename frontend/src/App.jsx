// src/App.jsx
import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import ThemeToggle from "./components/ThemeToggle";
import Login from "./pages/Login";
import TeacherDashboard from "./pages/TeacherDashboard";
import StudentView from "./pages/StudentView";
import HomeworkHelp from "./pages/HomeworkHelp";
import ExamPrep from "./pages/ExamPrep";
import AdaptiveLearning from "./pages/AdaptiveLearning";
import StudentUpload from "./pages/StudentUpload";

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <nav style={{ 
          padding: '15px 30px', 
          borderBottom: "2px solid var(--border-color)",
          backgroundColor: 'var(--nav-bg)',
          display: 'flex',
          gap: '20px',
          alignItems: 'center',
          transition: 'all 0.3s ease'
        }}>
          <Link to="/" style={{ fontWeight: 'bold', fontSize: '18px', textDecoration: 'none', color: 'var(--primary-color)' }}>
            🎓 Full Stack Tutoring AI
          </Link>
          <Link to="/login" style={{ textDecoration: 'none', color: 'var(--text-color)' }}>Login</Link>
          <Link to="/teacher" style={{ textDecoration: 'none', color: 'var(--text-color)' }}>Teacher</Link>
          <Link to="/student" style={{ textDecoration: 'none', color: 'var(--text-color)' }}>Chat</Link>
          <Link to="/upload" style={{ textDecoration: 'none', color: 'var(--text-color)' }}>📤 Upload</Link>
          <Link to="/homework" style={{ textDecoration: 'none', color: 'var(--text-color)' }}>Homework Help</Link>
          <Link to="/exam" style={{ textDecoration: 'none', color: 'var(--text-color)' }}>Exam Prep</Link>
          <Link to="/adaptive" style={{ textDecoration: 'none', color: 'var(--text-color)' }}>My Learning</Link>
          <div style={{ marginLeft: 'auto' }}>
            <ThemeToggle />
          </div>
        </nav>
      <div style={{ padding: 0, backgroundColor: 'var(--bg-primary)', minHeight: '100vh' }}>
        <Routes>
          <Route path="/" element={
            <div style={{ maxWidth: '800px', margin: '60px auto', padding: '40px', textAlign: 'center', color: 'var(--text-color)' }}>
              <h1 style={{ fontSize: '48px', marginBottom: '20px', color: 'var(--text-color)' }}>🎓 Welcome to Full Stack Tutoring AI</h1>
              <p style={{ fontSize: '20px', color: 'var(--text-secondary)', marginBottom: '40px' }}>
                Your intelligent learning companion powered by AI
              </p>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginTop: '40px' }}>
                <div style={{ padding: '30px', backgroundColor: 'var(--bg-card)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>💬</div>
                  <h3 style={{ color: 'var(--text-color)' }}>AI Chat</h3>
                  <p style={{ color: 'var(--text-secondary)' }}>Ask questions about your course materials</p>
                </div>
                <div style={{ padding: '30px', backgroundColor: 'var(--bg-card)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>📚</div>
                  <h3 style={{ color: 'var(--text-color)' }}>Homework Help</h3>
                  <p style={{ color: 'var(--text-secondary)' }}>Get step-by-step solutions with hints</p>
                </div>
                <div style={{ padding: '30px', backgroundColor: 'var(--bg-card)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>🎯</div>
                  <h3 style={{ color: 'var(--text-color)' }}>Exam Prep</h3>
                  <p style={{ color: 'var(--text-secondary)' }}>Practice with adaptive quizzes</p>
                </div>
                <div style={{ padding: '30px', backgroundColor: 'var(--bg-card)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>🎓</div>
                  <h3 style={{ color: 'var(--text-color)' }}>Adaptive Learning</h3>
                  <p style={{ color: 'var(--text-secondary)' }}>Personalized lessons based on your performance</p>
                </div>
              </div>
            </div>
          } />
          <Route path="/login" element={<Login />} />
          <Route path="/teacher" element={<TeacherDashboard />} />
          <Route path="/student" element={<StudentView />} />
          <Route path="/upload" element={<StudentUpload />} />
          <Route path="/homework" element={<HomeworkHelp />} />
          <Route path="/exam" element={<ExamPrep />} />
          <Route path="/exam-prep" element={<ExamPrep />} />
          <Route path="/adaptive" element={<AdaptiveLearning />} />
        </Routes>
      </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}
