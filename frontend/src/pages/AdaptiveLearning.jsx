import React, { useState, useEffect } from 'react';

function AdaptiveLearning() {
  const [recommendations, setRecommendations] = useState(null);
  const [lesson, setLesson] = useState(null);
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(true);
  const [lessonLoading, setLessonLoading] = useState(false);
  const [error, setError] = useState(null);

  const userId = "student_demo";

  // Fetch recommendations on load
  useEffect(() => {
    setLoading(true);
    fetch(`http://127.0.0.1:8000/api/learning/recommendations/${userId}`)
      .then(res => {
        if (!res.ok) throw new Error('No quiz data found');
        return res.json();
      })
      .then(data => {
        setRecommendations(data);
        setError(null);
      })
      .catch(err => {
        console.error("Failed to load recommendations:", err);
        setError("Take a quiz first to see your personalized learning dashboard!");
      })
      .finally(() => setLoading(false));
  }, []);

  const generateLesson = async () => {
    setLessonLoading(true);
    setLesson(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/learning/lesson", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, topic: topic || null }),
      });

      const data = await response.json();
      setLesson(data);
    } catch (error) {
      console.error("Error generating lesson:", error);
      alert("Failed to generate lesson. Make sure you have uploaded course materials.");
    } finally {
      setLessonLoading(false);
    }
  };

  const getPerformanceColor = (level) => {
    if (level === 'advanced') return '#28a745';
    if (level === 'average') return '#ffc107';
    return '#dc3545';
  };

  const getPerformanceIcon = (level) => {
    if (level === 'advanced') return '🌟';
    if (level === 'average') return '📈';
    return '💪';
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <h1>🎓 Adaptive Learning</h1>
      <p style={{ color: '#666', marginBottom: '30px' }}>
        Your personalized learning experience based on your performance
      </p>

      {/* Loading State */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '60px', color: '#666' }}>
          <div style={{ fontSize: '48px', marginBottom: '20px' }}>⏳</div>
          <p>Loading your learning dashboard...</p>
        </div>
      )}

      {/* Empty State - No Quiz Data */}
      {!loading && error && (
        <div style={{
          textAlign: 'center',
          padding: '60px 20px',
          backgroundColor: '#f8f9fa',
          borderRadius: '12px',
          border: '2px dashed #007bff'
        }}>
          <div style={{ fontSize: '64px', marginBottom: '20px' }}>📊</div>
          <h2 style={{ color: '#007bff', marginBottom: '15px' }}>No Performance Data Yet</h2>
          <p style={{ fontSize: '18px', color: '#666', marginBottom: '30px' }}>
            {error}
          </p>
          <div style={{
            backgroundColor: 'white',
            padding: '30px',
            borderRadius: '8px',
            maxWidth: '600px',
            margin: '0 auto',
            textAlign: 'left'
          }}>
            <h3 style={{ marginTop: 0 }}>🚀 Get Started:</h3>
            <ol style={{ lineHeight: '2', fontSize: '16px' }}>
              <li>Go to <strong>Exam Prep</strong></li>
              <li>Generate and take a quiz</li>
              <li>Submit your answers</li>
              <li>Come back here to see your personalized learning plan!</li>
            </ol>
          </div>
        </div>
      )}

      {/* Performance Dashboard */}
      {!loading && recommendations && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '20px',
          marginBottom: '30px'
        }}>
          {/* Performance Level Card */}
          <div style={{
            backgroundColor: getPerformanceColor(recommendations.performance_level),
            color: 'white',
            padding: '30px',
            borderRadius: '12px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '10px' }}>
              {getPerformanceIcon(recommendations.performance_level)}
            </div>
            <h2 style={{ margin: '10px 0', textTransform: 'capitalize' }}>
              {recommendations.performance_level}
            </h2>
            <p style={{ margin: 0, opacity: 0.9 }}>Performance Level</p>
          </div>

          {/* Average Score Card */}
          <div style={{
            backgroundColor: '#007bff',
            color: 'white',
            padding: '30px',
            borderRadius: '12px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '48px', fontWeight: 'bold', marginBottom: '10px' }}>
              {recommendations.avg_score.toFixed(1)}%
            </div>
            <h3 style={{ margin: '10px 0' }}>Average Score</h3>
            <p style={{ margin: 0, opacity: 0.9 }}>Across all quizzes</p>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {!loading && recommendations && (
        <div style={{
          backgroundColor: '#f8f9fa',
          padding: '30px',
          borderRadius: '12px',
          marginBottom: '30px'
        }}>
          <h2 style={{ marginTop: 0 }}>📚 Personalized Recommendations</h2>
          <ul style={{ lineHeight: '2', fontSize: '16px' }}>
            {recommendations.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>

          <h3 style={{ marginTop: '30px', marginBottom: '15px' }}>🎯 Suggested Topics</h3>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            {recommendations.next_topics.map((topic, index) => (
              <span
                key={index}
                style={{
                  padding: '8px 16px',
                  backgroundColor: '#007bff',
                  color: 'white',
                  borderRadius: '20px',
                  fontSize: '14px'
                }}
              >
                {topic}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Generate Adaptive Lesson */}
      {!loading && !error && (
        <div style={{
          backgroundColor: 'white',
          padding: '30px',
          borderRadius: '12px',
          border: '2px solid #dee2e6'
        }}>
          <h2 style={{ marginTop: 0 }}>📖 Generate Adaptive Lesson</h2>
          <p style={{ color: '#666', marginBottom: '20px' }}>
            Get a personalized lesson tailored to your learning level
          </p>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '10px' }}>
              Topic (optional):
            </label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Leave blank for general content"
              style={{
                width: '100%',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid #ccc',
                fontSize: '16px'
              }}
              disabled={lessonLoading}
            />
          </div>

          <button
            onClick={generateLesson}
            disabled={lessonLoading}
            style={{
              padding: '12px 24px',
              backgroundColor: lessonLoading ? '#ccc' : '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              cursor: lessonLoading ? 'not-allowed' : 'pointer',
              fontWeight: 'bold'
            }}
          >
            {lessonLoading ? 'Generating Lesson...' : '🚀 Generate Lesson'}
          </button>
        </div>
      )}

      {/* Display Generated Lesson */}
      {lesson && (
        <div style={{
          backgroundColor: '#f8f9fa',
          padding: '30px',
          borderRadius: '12px',
          marginTop: '30px',
          border: '2px solid #007bff'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '20px'
          }}>
            <h2 style={{ margin: 0 }}>
              {lesson.topic}
            </h2>
            <span style={{
              padding: '6px 12px',
              backgroundColor: getPerformanceColor(lesson.performance_level),
              color: 'white',
              borderRadius: '20px',
              fontSize: '14px',
              textTransform: 'capitalize'
            }}>
              {lesson.performance_level} Level
            </span>
          </div>

          <div style={{
            backgroundColor: 'white',
            padding: '25px',
            borderRadius: '8px',
            whiteSpace: 'pre-wrap',
            lineHeight: '1.8',
            fontSize: '16px'
          }}>
            {lesson.lesson}
          </div>

          <div style={{
            marginTop: '20px',
            padding: '15px',
            backgroundColor: '#e7f3ff',
            borderRadius: '8px',
            fontSize: '14px',
            color: '#004085'
          }}>
            💡 <strong>Tip:</strong> This lesson was customized for your {lesson.performance_level} level
            (Average Score: {lesson.avg_score.toFixed(1)}%)
          </div>
        </div>
      )}
    </div>
  );
}

export default AdaptiveLearning;
