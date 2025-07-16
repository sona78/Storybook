import React, { useEffect, useState, useRef } from 'react';
import HTMLFlipBook from 'react-pageflip';
import './App.css';

function App() {
  const [promptSections, setPromptSections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const pageRef = useRef(null);

  useEffect(() => {
    loadPrompt();
    // eslint-disable-next-line
  }, []);

  const loadPrompt = () => {
    setLoading(true);
    setError('');
    fetch('/api/combined-prompt')
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          setPromptSections([]);
        } else {
          // Split prompt into sections by double newlines or single newlines
          const sections = data.prompt ? data.prompt.split(/\n+/).filter(Boolean) : [];
          setPromptSections(sections);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError('Failed to load prompt: ' + err.message);
        setPromptSections([]);
        setLoading(false);
      });
  };

  // Use an online old paper texture image
  const texturedPageUrl =
    'https://www.transparenttextures.com/patterns/old-mathematics.png';

  // Brownish old paper color
  const oldPaperColor = '#f5ecd7'; // Lighter, more paper-like
  const oldPaperTextColor = '#3e2c1a'; // Deep brown for text

  // Slightly off-white background for the app, not pure black
  const appBackground = '#e9e4d8';

  return (
    <div
      style={{
        background: appBackground,
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    >
      {loading ? (
        <div className="loading-message" style={{ color: '#3e2c1a' }}>Loading...</div>
      ) : error ? (
        <div className="error-message" style={{ color: 'red' }}>{error}</div>
      ) : (
        <HTMLFlipBook
          width={350}
          height={500}
          ref={pageRef}
          style={{
            boxShadow: '0 8px 32px 0 rgba(0,0,0,0.18)',
            borderRadius: '10px',
            background: oldPaperColor
          }}
        >
          {promptSections.length === 0 ? (
            <div
              className="page"
              style={{
                backgroundColor: oldPaperColor,
                backgroundImage: `url(${texturedPageUrl})`,
                backgroundSize: 'auto',
                backgroundRepeat: 'repeat',
                color: oldPaperTextColor,
                fontFamily: '"Times New Roman", Times, serif',
                padding: '2em',
                minHeight: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 2px 8px 0 rgba(60,40,20,0.10)'
              }}
            >
              <span>No story to display.</span>
            </div>
          ) : (
            promptSections.map((section, idx) => (
              <div
                key={idx}
                className="page"
                style={{
                  backgroundColor: oldPaperColor,
                  backgroundImage: `url(${texturedPageUrl})`,
                  backgroundSize: 'auto',
                  backgroundRepeat: 'repeat',
                  color: oldPaperTextColor,
                  fontFamily: '"Times New Roman", Times, serif',
                  padding: '2em',
                  minHeight: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.1em',
                  lineHeight: '1.6',
                  boxShadow: '0 2px 8px 0 rgba(60,40,20,0.10)'
                }}
              >
                <span>{section}</span>
              </div>
            ))
          )}
        </HTMLFlipBook>
      )}
    </div>
  );
}

export default App;
