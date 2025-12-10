import React, { useState, useEffect, useRef } from "react";
import { useAppContext } from "../context/AppContext";
import LoadingSpinner from "../components/LoadingSpinner";
import { useLocation } from "react-router-dom";

export default function ExamPrep() {
  const { topic, uploadedFile } = useAppContext();
  const [customTopic, setCustomTopic] = useState(topic || "");
  const [loading, setLoading] = useState(false);
  const [quiz, setQuiz] = useState(null);
  const [error, setError] = useState(null);
  
  const location = useLocation();
  const hasAutoStarted = useRef(false);

  // Quiz taking state
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (topic) setCustomTopic(topic);
  }, [topic]);

  // Auto-start quiz if coming from upload page with flag
  useEffect(() => {
    if (location.state?.autoStart && !hasAutoStarted.current) {
        if (uploadedFile || topic) {
            console.log("🚀 Auto-starting quiz generation from upload...");
            hasAutoStarted.current = true;
            generateQuiz();
        }
    }
  }, [location.state, uploadedFile, topic]);

  const generateQuiz = async () => {
    setLoading(true);
    setError(null);
    setQuiz(null);
    setAnswers({});
    setSubmitted(false);
    setResults(null);
    
    // Use the topic state if available, otherwise custom input
    const topicToUse = customTopic || topic || "General";
    
    try {
      const res = await fetch("http://127.0.0.1:8000/api/exam/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: topicToUse,
          file_id: uploadedFile?.file_id || null,
          num_questions: 5,
        }),
      });
      
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || `Quiz generation failed: ${res.status}`);
      }
      
      const data = await res.json();
      console.log("Quiz data received:", data);
      setQuiz(data);
    } catch (err) {
      console.error("Generate quiz error", err);
      setError(err.message || "Quiz generation failed");
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, selectedAnswer) => {
    setAnswers({
      ...answers,
      [questionId]: selectedAnswer
    });
  };

  const submitQuiz = async () => {
    if (!quiz || Object.keys(answers).length === 0) {
      setError("Please answer at least one question before submitting");
      return;
    }

    setSubmitting(true);
    setError(null);
    
    try {
      // Format answers for backend
      const formattedAnswers = Object.entries(answers).map(([qId, answer]) => ({
        question_id: parseInt(qId),
        answer: answer
      }));

      const res = await fetch("http://127.0.0.1:8000/api/exam/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "student_demo",
          quiz_id: quiz.quiz_id,
          answers: formattedAnswers
        }),
      });

      if (!res.ok) {
        const txt = await res.text();
        throw new Error(txt || `Quiz submission failed: ${res.status}`);
      }

      const data = await res.json();
      console.log("Quiz results:", data);
      setResults(data);
      setSubmitted(true);
    } catch (err) {
      console.error("Submit quiz error", err);
      setError(err.message || "Quiz submission failed");
    } finally {
      setSubmitting(false);
    }
  };

  const getPerformanceBadge = (level) => {
    switch(level) {
      case "advanced":
        return <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full font-semibold">🟢 Advanced</span>;
      case "average":
        return <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full font-semibold">🟡 Average</span>;
      case "struggling":
        return <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full font-semibold">🔴 Below Average</span>;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {loading && <LoadingSpinner message="🎯 Antigravity is crafting your personalized quiz based on your document..." />}
      {submitting && <LoadingSpinner message="📊 Grading your quiz..." />}
      
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">📝 Exam Prep</h1>
        
        {/* Topic Input and Generate Button */}
        {!quiz && !loading && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <label className="block text-lg font-semibold text-gray-700 mb-2">Topic</label>
            <input
              value={customTopic}
              onChange={(e) => setCustomTopic(e.target.value)}
              className="w-full border border-gray-300 rounded-lg p-3 mb-4 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="Enter a topic or it will auto-fill from uploaded document"
            />
            <button 
              onClick={generateQuiz} 
              className="w-full px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition disabled:opacity-50 disabled:cursor-not-allowed" 
              disabled={loading}
            >
              {loading ? "Generating Quiz..." : "Generate Quiz"}
            </button>
            {uploadedFile && (
                <p className="mt-2 text-sm text-green-600">✅ Using uploaded document: {uploadedFile.original_filename}</p>
            )}
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">❌ {error}</p>
          </div>
        )}

        {/* Interactive Quiz */}
        {quiz && !submitted && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-indigo-700 mb-2">
                {quiz.quiz_title || "Quiz"}
              </h2>
              <p className="text-gray-600">Answer all {quiz.total_questions} questions and submit to see your score.</p>
            </div>

            {quiz.questions && quiz.questions.map((q, index) => (
              <div key={q.id || index} className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                <p className="text-lg font-semibold text-gray-800 mb-3">
                  {index + 1}. {q.question}
                </p>
                
                <div className="space-y-2">
                  {q.options && q.options.map((option, optIndex) => (
                    <label 
                      key={optIndex} 
                      className="flex items-center p-3 rounded-lg border border-gray-300 hover:bg-indigo-50 cursor-pointer transition"
                    >
                      <input
                        type="radio"
                        name={`question-${q.id || index}`}
                        value={option}
                        checked={answers[q.id || (index + 1)] === option}
                        onChange={() => handleAnswerSelect(q.id || (index + 1), option)}
                        className="mr-3 w-4 h-4 text-indigo-600"
                      />
                      <span className="text-gray-700">{option}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}

            <div className="mt-6 flex gap-4">
              <button
                onClick={submitQuiz}
                disabled={submitting || Object.keys(answers).length === 0}
                className="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? "Submitting..." : "Submit Quiz"}
              </button>
              <button
                onClick={() => { setQuiz(null); setAnswers({}); }}
                className="px-6 py-3 bg-gray-500 text-white rounded-lg font-semibold hover:bg-gray-600 transition"
              >
                Start Over
              </button>
            </div>
          </div>
        )}

        {/* Results and Adaptive Learning */}
        {submitted && results && (
          <div className="space-y-6">
            {/* Score Card */}
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow-lg p-8 text-white">
              <h2 className="text-3xl font-bold mb-4">🎉 Quiz Complete!</h2>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-indigo-100 text-sm">Your Score</p>
                  <p className="text-5xl font-bold">{results.percentage}</p>
                </div>
                <div>
                  <p className="text-indigo-100 text-sm">Correct Answers</p>
                  <p className="text-3xl font-bold">{results.correct_answers} / {results.total_questions}</p>
                </div>
              </div>
              <div className="mt-4">
                <p className="text-indigo-100 text-sm mb-2">Performance Level</p>
                {getPerformanceBadge(results.performance_level)}
              </div>
            </div>

            {/* Adaptive Learning Recommendations */}
            {results.recommendations && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-2xl font-bold text-gray-800 mb-4">🎓 Your Personalized Learning Path</h3>
                <div className="space-y-3">
                  {results.recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start p-4 bg-indigo-50 rounded-lg">
                      <span className="text-indigo-600 mr-3 text-xl">✓</span>
                      <p className="text-gray-700">{rec}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-4">
              <button
                onClick={() => { setQuiz(null); setAnswers({}); setSubmitted(false); setResults(null); }}
                className="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition"
              >
                Take Another Quiz
              </button>
              <button
                onClick={() => window.location.href = '/adaptive'}
                className="flex-1 px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition"
              >
                View Adaptive Lessons
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
