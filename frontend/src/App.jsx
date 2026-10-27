import { Component } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import Editor from "./pages/CodeEditor";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: 32,
          background: "#121212",
          color: "#eff1f6",
          fontFamily: "system-ui, -apple-system, sans-serif",
          height: "100vh",
          width: "100vw",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 16,
          boxSizing: "border-box"
        }}>
          <div style={{
            background: "#1a1a1a",
            border: "1px solid #333",
            borderRadius: 8,
            padding: 24,
            maxWidth: 600,
            width: "90%",
            textAlign: "center"
          }}>
            <h2 style={{ fontSize: 18, color: "#ff375f", marginBottom: 10 }}>Interface Rendering Notice</h2>
            <p style={{ fontSize: 13, color: "#a1a1aa", marginBottom: 16, lineHeight: 1.5 }}>
              The application encountered an issue while loading. Please try reloading the page.
            </p>
            <pre style={{
              background: "#121212",
              border: "1px solid #2a2a2a",
              padding: 12,
              borderRadius: 6,
              fontSize: 11.5,
              color: "#fbbf24",
              textAlign: "left",
              overflowX: "auto",
              marginBottom: 16,
              fontFamily: "monospace"
            }}>
              {this.state.error?.toString()}
            </pre>
            <button
              onClick={() => window.location.reload()}
              style={{
                padding: "8px 20px",
                background: "#2cbb5d",
                color: "#ffffff",
                borderRadius: 6,
                border: "none",
                cursor: "pointer",
                fontWeight: 600,
                fontSize: 13
              }}
            >
              Reload SCRS
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

const App = () => {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Editor />} />
        </Routes>
      </BrowserRouter>
    </ErrorBoundary>
  );
};

export default App;