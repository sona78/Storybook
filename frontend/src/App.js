import './App.css';
import React, { useEffect, useState, useRef } from 'react';
import HTMLFlipBook from 'react-pageflip';

function App() {
  const [promptSections, setPromptSections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isBookReady, setIsBookReady] = useState(false);
  const pageRef = useRef(null);
  const bookDivRef = useRef(null);
  const [title, setTitle] = useState("")
  const [prompt, setPrompt] = useState("")

  useEffect(() => {
    loadPrompt();
    
    // Cleanup function to handle component unmounting
    return () => {
      if (pageRef.current && pageRef.current.pageFlip) {
        try {
          pageRef.current.pageFlip().destroy();
        } catch (error) {
          console.warn('Error destroying flipbook:', error);
        }
      }
    };
    // eslint-disable-next-line
  }, []);

  const loadPrompt = () => {
    setLoading(true);
    setError('');
    setIsBookReady(false);
    fetch('/api/storybook')
      .then((response) => response.json())
      .then((data) => {
        console.log('Received data:', data);
        const story = data.story
        const title = data.title
        const prompt = data.prompt
        const sections = Array.isArray(story)
          ? story.map(entry => ({ content: entry.content, illustration: entry.image_url }))
          : [];
        console.log('Processed sections:', sections);
        setPromptSections(sections);
        setTitle(title)
        setPrompt(prompt)
        setLoading(false);
        // Small delay to ensure DOM is ready before rendering book
        setTimeout(() => setIsBookReady(true), 100);
      })
      .catch((err) => {
        setError('Failed to load prompt: ' + err.message);
        setPromptSections([]);
        setLoading(false);
      });
  };

  // Use an online old paper texture image
  const texturedPageUrl = 'https://www.transparenttextures.com/patterns/light-paper-fibers.png';

  // Brownish old paper color
  const oldPaperColor = '#f5ecd7'; // Lighter, more paper-like
  const oldPaperTextColor = '#3e2c1a'; // Deep brown for text

  // Cover page
  const Cover = React.forwardRef((props, ref) => {
    return (
      <div
        className='page'
        ref={ref}
        style={{
          position: "relative",
          background: `${oldPaperColor} url(${texturedPageUrl})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100%",
          width: "100%",
          minWidth: 0,
          minHeight: 0,
        }}
      >
        <div
          style={{
            borderRadius: "8px",
            padding: "40px 60px",
            textAlign: "center",
          }}
        >
          <h1
            style={{
              fontFamily: '"Times New Roman", Times, serif',
              color: "#5a4321",
              fontSize: "2.5rem",
              marginBottom: "0.5em",
              letterSpacing: "2px",
              textShadow: "0 2px 8px #e9e4d8",
            }}
          >
            {title}
          </h1>
          <h3
            style={{
              fontFamily: '"Times New Roman", Times, serif',
              color: "#7c6240",
              fontWeight: "normal",
              marginTop: "0",
              fontSize: "1.2rem",
              letterSpacing: "1px",
            }}
          >
            by You!
          </h3>
        </div>
      </div>
    );
  });

  // Content page
  const Page = React.forwardRef(({ entry, number }, ref) => {
    return (
      <div
        className="page"
        ref={ref}
        style={{
          background: `${oldPaperColor} url(${texturedPageUrl})`,
          backgroundSize: "cover",
          height: "100%",
          width: "100%",
          minWidth: 0,
          minHeight: 0,
          position: "relative",
          display: "flex",
          flexDirection: "column",
          boxSizing: "border-box",
        }}
      >
        <div
          className="image-section"
          style={{
            width: '80%',
            border: '1px solid #d0c8b8',
            margin: '20px auto',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: '4px',
            background: "#f3e7c6",
          }}
        >
          {entry?.illustration && (
            <img
              src={entry.illustration}
              alt="Story page illustration"
              style={{
                width: '100%',
                height: '100%',
                maxWidth: '100%',
                maxHeight: '100%',
                aspectRatio: '1 / 1',
                objectFit: 'cover',
                borderRadius: '4px',
                display: 'block'
              }}
            />
          )}
        </div>
        <div
          className="text-content"
          style={{
            fontFamily: '"Times New Roman", Times, serif',
            lineHeight: '1.5',
            marginBottom: 40,
            padding: 20,
            color: oldPaperTextColor,
            flex: 1,
            fontSize: "1.1rem",
            textAlign: "left"
          }}
        >
          {entry?.content}
        </div>
        <div
          className="page-number"
          style={{
            position: 'absolute',
            bottom: '20px',
            right: '20px',
            fontFamily: '"Times New Roman", Times, serif',
            fontSize: '14px',
            color: '#6b5b47',
            fontWeight: 'normal'
          }}
        >
          Page {number}
        </div>
      </div>
    );
  });

  // Back cover page
  const BackCover = React.forwardRef((props, ref) => {
    return (
      <div
        className='page'
        ref={ref}
        style={{
          position: "relative",
          background: `${oldPaperColor} url(${texturedPageUrl})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100%",
          width: "100%",
          minWidth: 0,
          minHeight: 0,
        }}
      >
        <div
          style={{
            borderRadius: "8px",
            padding: "40px 60px",
            textAlign: "center",
            color: "#7c6240",
            fontFamily: '"Times New Roman", Times, serif',
            fontSize: "1.3rem"
          }}
        >
          <h1>The End</h1>
        </div>
      </div>
    );
  });

  // Navigation handlers
  const nextPage = () => {
    if (pageRef.current && pageRef.current.pageFlip) {
      try {
        pageRef.current.pageFlip().flipNext();
      } catch (error) {
        console.warn('Error flipping to next page:', error);
      }
    }
  };
  const prevPage = () => {
    if (pageRef.current && pageRef.current.pageFlip) {
      try {
        pageRef.current.pageFlip().flipPrev();
      } catch (error) {
        console.warn('Error flipping to previous page:', error);
      }
    }
  };

  // Keyboard navigation for accessibility
  React.useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "ArrowLeft") {
        prevPage();
      } else if (e.key === "ArrowRight") {
        nextPage();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
    // eslint-disable-next-line
  }, []);

  // Touch swipe navigation for mobile (using ref, not document.getElementById)
  React.useEffect(() => {
    if (!isBookReady) return;

    let touchStartX = null;
    let touchEndX = null;

    const handleTouchStart = (e) => {
      touchStartX = e.changedTouches[0].screenX;
    };
    const handleTouchEnd = (e) => {
      touchEndX = e.changedTouches[0].screenX;
      if (touchStartX !== null && touchEndX !== null) {
        if (touchEndX - touchStartX > 60) {
          prevPage();
        } else if (touchStartX - touchEndX > 60) {
          nextPage();
        }
      }
      touchStartX = null;
      touchEndX = null;
    };

    const bookDiv = bookDivRef.current;
    if (bookDiv) {
      bookDiv.addEventListener("touchstart", handleTouchStart);
      bookDiv.addEventListener("touchend", handleTouchEnd);
    }
    return () => {
      if (bookDiv) {
        bookDiv.removeEventListener("touchstart", handleTouchStart);
        bookDiv.removeEventListener("touchend", handleTouchEnd);
      }
    };
    // eslint-disable-next-line
  }, [isBookReady, promptSections]);

  // Total pages: cover + content + back cover
  const totalPages = 2 + promptSections.length;

  return (
    <div
      style={{
        minHeight: '100vh',
        width: '100vw',
        background: '#fff',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'flex-start',
        padding: '0',
        boxSizing: 'border-box'
      }}
    >
      <header
        style={{
          width: "100%",
          padding: "40px 0 24px 0",
          textAlign: "center",
          background: "transparent",
        }}
      >
        <h1
          style={{
            fontFamily: '"Times New Roman", Times, serif',
            fontSize: "2.8rem",
            color: "#3e2c1a",
            margin: 0,
            letterSpacing: "2px",
            fontWeight: 700,
            textShadow: "0 2px 8px #e9e4d8",
          }}
        >
          Storybook
        </h1>
        <p
          style={{
            color: "#7c6240",
            fontFamily: '"Times New Roman", Times, serif',
            fontSize: "1.1rem",
            margin: "8px 0 0 0",
            letterSpacing: "1px"
          }}
        >
          Swipe or use arrows to turn the pages
        </p>
      </header>
      <main
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
        }}
      >
        {loading ? (
          <div className="loading-message" style={{ color: '#3e2c1a', fontSize: "1.2rem" }}>Loading...</div>
        ) : error ? (
          <div className="error-message" style={{ color: 'red', fontSize: "1.2rem" }}>{error}</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: "100%" }}>
            <div
              ref={bookDivRef}
              style={{
                width: 350,
                height: 500,
                boxShadow: "0 8px 32px 0 rgba(60,40,20,0.18), 0 1.5px 8px 0 rgba(60,40,20,0.10)",
                borderRadius: "18px",
                background: "#f5ecd7",
                position: "relative",
                overflow: "hidden",
                flexShrink: 0,
                flexGrow: 0,
                margin: "0 auto",
                transition: "box-shadow 0.2s",
                outline: "none"
              }}
              tabIndex={0}
              aria-label="Storybook flipbook"
            >
              {isBookReady && (
                <HTMLFlipBook
                  width={350}
                  height={500}
                  ref={pageRef}
                  showCover={true}
                  style={{
                    width: "100%",
                    height: "100%",
                    minWidth: 350,
                    minHeight: 500,
                    maxWidth: 350,
                    maxHeight: 500,
                    boxShadow: "none",
                    background: "transparent"
                  }}
                  maxShadowOpacity={0.4}
                  mobileScrollSupport={true}
                  useMouseEvents={true}
                  flippingTime={600}
                  startPage={0}
                  size="fixed"
                  minWidth={350}
                  minHeight={500}
                  maxWidth={350}
                  maxHeight={500}
                  drawShadow={true}
                  disableFlipByClick={false}
                  key={`flipbook-${promptSections.length}-${Date.now()}`}
                >
                  <Cover key="cover" />
                  {promptSections.map((section, idx) => (
                    <Page
                      key={`page-${idx}-${section.content?.substring(0, 10)}`}
                      number={idx + 1}
                      entry={section}
                    />
                  ))}
                  <BackCover key="backcover" />
                </HTMLFlipBook>
              )}
            </div>
            <div style={{
              marginTop: 28,
              display: 'flex',
              gap: 18,
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <button
                className="book-btn"
                onClick={prevPage}
                aria-label="Previous page"
                style={{
                  background: "#fff",
                  color: "#3e2c1a",
                  border: "1.5px solid #bba77a",
                  borderRadius: "50%",
                  width: 48,
                  height: 48,
                  fontSize: "1.5rem",
                  fontFamily: '"Times New Roman", Times, serif',
                  cursor: "pointer",
                  boxShadow: "0 2px 8px #bba77a33",
                  transition: "background 0.2s, box-shadow 0.2s",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  outline: "none"
                }}
              >
                &#8592;
              </button>
              <span style={{
                fontFamily: '"Times New Roman", Times, serif',
                color: "#7c6240",
                fontSize: "1.1rem",
                minWidth: 80,
                textAlign: "center"
              }}>
                Page {promptSections.length === 0 ? 1 : undefined}
              </span>
              <button
                className="book-btn"
                onClick={nextPage}
                aria-label="Next page"
                style={{
                  background: "#fff",
                  color: "#3e2c1a",
                  border: "1.5px solid #bba77a",
                  borderRadius: "50%",
                  width: 48,
                  height: 48,
                  fontSize: "1.5rem",
                  fontFamily: '"Times New Roman", Times, serif',
                  cursor: "pointer",
                  boxShadow: "0 2px 8px #bba77a33",
                  transition: "background 0.2s, box-shadow 0.2s",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  outline: "none"
                }}
              >
                &#8594;
              </button>
            </div>
            <div style={{
              marginTop: 16,
              color: "#bba77a",
              fontFamily: '"Times New Roman", Times, serif',
              fontSize: "0.95rem",
              opacity: 0.7
            }}>
              Tip: You can swipe, click, or use your keyboard arrows to turn the pages!
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
