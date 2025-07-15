import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import { Card, Container, Row, Col, Button } from 'react-bootstrap';
import './App.css';

function App() {
  const [promptSections, setPromptSections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

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

  const copyToClipboard = () => {
    const text = promptSections.join('\n');
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!');
      }).catch(err => {
        showNotification('Failed to copy: ' + err);
      });
    } else {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      showNotification('Copied to clipboard!');
    }
  };

  const downloadPrompt = () => {
    const text = promptSections.join('\n');
    if (text && !loading && !error && !text.includes('No content found')) {
      const blob = new Blob([text], { type: 'text/plain' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'combined-prompt.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      showNotification('Download started!');
    } else {
      showNotification('No content to download');
    }
  };

  const showNotification = (message) => {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #28a745;
      color: white;
      padding: 10px 20px;
      border-radius: 5px;
      z-index: 1000;
      animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => {
        document.body.removeChild(notification);
      }, 300);
    }, 2000);
  };

  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
      @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
      }
      .hover-card {
        transition: box-shadow 0.3s, transform 0.3s;
        cursor: pointer;
      }
      .hover-card:hover {
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3), 0 1.5px 6px rgba(0,0,0,0.08);
        transform: translateY(-4px) scale(1.03);
        background: #f0f4ff;
      }
      .card-index {
        display: none;
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 1.2rem;
        color: #764ba2;
        font-weight: bold;
      }
      .hover-card:hover .card-index {
        display: block;
      }
    `;
    document.head.appendChild(style);
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <Container className="container mt-5">
      <div className="header">
        <h1>CrowdWork</h1>
        <p>Combined Prompt Viewer</p>
      </div>
      <div className="canvas-container">
        {loading ? (
          <div className="loading">Loading combined prompt...</div>
        ) : error ? (
          <div className="error">Error: {error}</div>
        ) : promptSections.length === 0 ? (
          <div className="empty-state">No content found in database. Add some entries to see them here.</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {promptSections.map((section, idx) => (
              <Card
                key={idx}
                className="hover-card position-relative mb-3"
                style={{ width: '100%' }}
              >
                <Card.Body>
                  <span className="card-index">#{idx + 1}</span>
                  <Card.Text style={{ whiteSpace: 'pre-wrap' }}>{section}</Card.Text>
                </Card.Body>
              </Card>
            ))}
          </div>
        )}
      </div>
      <div className="controls mt-4">
        <Button variant="primary" onClick={loadPrompt}>Refresh Prompt</Button>
        <Button variant="secondary" onClick={copyToClipboard}>Copy to Clipboard</Button>
        <Button variant="secondary" onClick={downloadPrompt}>Download as TXT</Button>
      </div>
    </Container>
  );
}

export default App;
