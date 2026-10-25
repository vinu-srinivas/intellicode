import React, { useEffect, useRef, useState } from "react";
import Editor from "@monaco-editor/react";
import { loadPyodide } from "pyodide";

const CodeEditor = () => {
  const [tab, setTab] = useState("main.py");
  const [isExpanded, setIsExpanded] = useState(false);
  const [pythonCode, setPythonCode] = useState(
`print("Hello World!")
`
  );
  const [output, setOutput] = useState("");
  const [hasError, setHasError] = useState(false);
  const [isPythonReady, setIsPythonReady] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [runCount, setRunCount] = useState(0);
  const [lastRunTime, setLastRunTime] = useState(null);
  const pyodideRef = useRef(null);

  useEffect(() => {
    const init = async () => {
      try {
        const pyodide = await loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v314.0.6/full/",
        });
        pyodideRef.current = pyodide;
        setIsPythonReady(true);
        setOutput("intellicode engine ready.\n");
      } catch (err) {
        setOutput("failed to load python: " + err.toString());
        setHasError(true);
      }
    };
    init();
  }, []);

  const runPython = async () => {
    if (!pyodideRef.current) return;
    setIsRunning(true);
    setOutput("");
    setHasError(false);

    const pyodide = pyodideRef.current;
    let captured = "";
    pyodide.setStdout({ batched: (t) => (captured += t) });
    pyodide.setStderr({ batched: (t) => (captured += t) });

    const startTime = performance.now();

    try {
      const result = await pyodide.runPythonAsync(pythonCode);
      if (result !== undefined && result !== null) captured += String(result);
      setOutput(captured || "(program executed with no output)");
    } catch (err) {
      setOutput(captured + "\n" + err.toString());
      setHasError(true);
    }

    const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);
    setLastRunTime(elapsed);
    setRunCount((c) => c + 1);
    setIsRunning(false);
  };

  useEffect(() => {
    const handler = (e) => {
      if (e.ctrlKey && e.key === "Enter") {
        e.preventDefault();
        runPython();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [pythonCode, isPythonReady]);

  const downloadCode = () => {
    const blob = new Blob([pythonCode], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "main.py";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { margin: 0; overflow: hidden; background: #09090b; }

        .cf-root {
          height: 100vh;
          display: flex;
          flex-direction: column;
          background: #09090b;
          color: #a1a1aa;
          font-family: 'Inter', sans-serif;
        }

        /* ---- top bar ---- */
        .cf-topbar {
          height: 52px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 20px;
          background: #09090b;
          border-bottom: 1px solid #18181b;
          flex-shrink: 0;
          user-select: none;
        }

        .cf-logo {
          display: flex;
          align-items: center;
          gap: 10px;
          font-weight: 800;
          font-size: 15px;
          color: #fafafa;
          letter-spacing: -0.5px;
          cursor: pointer;
        }

        .cf-logo-badge {
          width: 28px;
          height: 28px;
          border-radius: 7px;
          background: #a855f7;
          display: flex;
          align-items: center;
          justify-content: center;
          font-family: 'JetBrains Mono', monospace;
          font-weight: 800;
          font-size: 12px;
          color: #ffffff;
          letter-spacing: -0.5px;
        }

        .cf-topbar-right {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .cf-btn-ghost {
          height: 30px;
          padding: 0 12px;
          background: transparent;
          border: 1px solid #27272a;
          border-radius: 6px;
          color: #71717a;
          font-size: 12px;
          font-family: 'Inter', sans-serif;
          font-weight: 500;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;
          transition: border-color 0.15s, color 0.15s;
        }
        .cf-btn-ghost:hover {
          border-color: #3f3f46;
          color: #d4d4d8;
        }

        /* ---- tabs bar ---- */
        .cf-tabs {
          height: 38px;
          display: flex;
          align-items: stretch;
          background: #09090b;
          border-bottom: 1px solid #18181b;
          padding-left: 12px;
          flex-shrink: 0;
          gap: 0;
        }

        .cf-tab {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 0 16px;
          font-size: 12px;
          font-family: 'JetBrains Mono', monospace;
          font-weight: 500;
          color: #52525b;
          cursor: pointer;
          border-bottom: 2px solid transparent;
          transition: color 0.1s;
          user-select: none;
          background: none;
          border-top: none;
          border-left: none;
          border-right: none;
        }
        .cf-tab:hover { color: #a1a1aa; }
        .cf-tab.active {
          color: #e4e4e7;
          border-bottom-color: #a855f7;
        }
        .cf-tab .dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #22c55e;
          opacity: 0.8;
          box-shadow: 0 0 8px #22c55e;
        }
        .cf-tab .dot.loading {
          background: #eab308;
          box-shadow: 0 0 8px #eab308;
          animation: pulse 1.5s ease infinite;
        }

        .cf-tabs-right {
          margin-left: auto;
          display: flex;
          align-items: center;
          padding-right: 12px;
          gap: 6px;
        }

        /* ---- run button ---- */
        .cf-run {
          height: 28px;
          padding: 0 14px;
          background: #a855f7;
          border: none;
          border-radius: 6px;
          color: #fff;
          font-size: 12px;
          font-weight: 600;
          font-family: 'Inter', sans-serif;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;
          transition: background 0.15s, opacity 0.15s;
          letter-spacing: 0.2px;
        }
        .cf-run:hover { background: #9333ea; }
        .cf-run:active { background: #7e22ce; }
        .cf-run:disabled {
          opacity: 0.4;
          cursor: not-allowed;
        }
        .cf-run:disabled:hover { background: #a855f7; }

        .cf-run .spinner {
          width: 12px;
          height: 12px;
          border: 2px solid #fff4;
          border-top-color: #fff;
          border-radius: 50%;
          animation: spin 0.6s linear infinite;
        }

        .cf-icon-btn {
          width: 28px;
          height: 28px;
          background: transparent;
          border: 1px solid transparent;
          border-radius: 5px;
          color: #52525b;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 14px;
          transition: all 0.12s;
        }
        .cf-icon-btn:hover {
          background: #18181b;
          color: #a1a1aa;
        }

        /* ---- main area ---- */
        .cf-main {
          display: flex;
          flex: 1;
          overflow: hidden;
        }

        .cf-editor-wrap {
          transition: width 0.2s ease;
          overflow: hidden;
          position: relative;
        }

        /* ---- output ---- */
        .cf-output-wrap {
          display: flex;
          flex-direction: column;
          background: #09090b;
          border-left: 1px solid #18181b;
          overflow: hidden;
        }

        .cf-output-header {
          height: 38px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 16px;
          border-bottom: 1px solid #18181b;
          flex-shrink: 0;
        }

        .cf-output-title {
          font-size: 11px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 1px;
          color: #3f3f46;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .cf-badge {
          font-size: 9px;
          font-weight: 700;
          padding: 1px 6px;
          border-radius: 3px;
          letter-spacing: 0.5px;
          font-family: 'JetBrains Mono', monospace;
        }
        .cf-badge.ok {
          background: #22c55e18;
          color: #22c55e;
        }
        .cf-badge.err {
          background: #ef444418;
          color: #ef4444;
        }

        .cf-output-body {
          flex: 1;
          overflow: auto;
          padding: 16px 20px;
        }

        .cf-output-body pre {
          margin: 0;
          font-family: 'JetBrains Mono', monospace;
          font-size: 12.5px;
          line-height: 1.7;
          white-space: pre-wrap;
          word-break: break-word;
          color: #a1a1aa;
        }
        .cf-output-body pre.error {
          color: #f87171;
        }
        .cf-output-body pre.empty {
          color: #27272a;
          font-style: italic;
        }

        /* ---- status bar ---- */
        .cf-statusbar {
          height: 26px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 16px;
          background: #09090b;
          border-top: 1px solid #18181b;
          font-size: 11px;
          font-family: 'JetBrains Mono', monospace;
          color: #27272a;
          flex-shrink: 0;
          user-select: none;
        }
        .cf-statusbar .left,
        .cf-statusbar .right {
          display: flex;
          align-items: center;
          gap: 16px;
        }
        .cf-statusbar .connected {
          color: #22c55e;
        }
        .cf-statusbar .disconnected {
          color: #eab308;
        }

        /* ---- running indicator bar ---- */
        .cf-run-indicator {
          height: 2px;
          background: linear-gradient(90deg, #a855f7, #ec4899, #a855f7);
          background-size: 200% 100%;
          animation: shimmer 1s ease-in-out infinite;
          position: absolute;
          bottom: 0;
          left: 0;
          right: 0;
          z-index: 10;
        }

        /* ---- scrollbar ---- */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #27272a; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #3f3f46; }

        ::selection {
          background: #a855f730;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 0.4; }
          50% { opacity: 1; }
        }
        @keyframes shimmer {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>

      <div className="cf-root">
        {/* ===== TOP BAR ===== */}
        <div className="cf-topbar">
          <div className="cf-logo">
            <div className="cf-logo-badge">ic</div>
            intellicode
          </div>
          <div className="cf-topbar-right">
            {runCount > 0 && (
              <span style={{ fontSize: 11, color: "#3f3f46", fontFamily: "'JetBrains Mono', monospace" }}>
                {runCount} run{runCount !== 1 ? "s" : ""}
                {lastRunTime && ` · ${lastRunTime}s`}
              </span>
            )}
            <button className="cf-btn-ghost" onClick={downloadCode}>
              ↓ save
            </button>
          </div>
        </div>

        {/* ===== TABS ===== */}
        <div className="cf-tabs">
          <button
            className={`cf-tab ${tab === "main.py" ? "active" : ""}`}
            onClick={() => setTab("main.py")}
          >
            <span className={`dot ${isPythonReady ? "" : "loading"}`} />
            main.py
          </button>

          <div className="cf-tabs-right">
            <button
              className="cf-run"
              onClick={runPython}
              disabled={!isPythonReady || isRunning}
            >
              {isRunning ? (
                <>
                  <span className="spinner" />
                  running
                </>
              ) : (
                <>▸ run</>
              )}
            </button>

            <button
              className="cf-icon-btn"
              onClick={() => setIsExpanded(!isExpanded)}
              title={isExpanded ? "show output" : "focus mode"}
            >
              {isExpanded ? "⊟" : "⊞"}
            </button>
          </div>
        </div>

        {/* ===== MAIN ===== */}
        <div className="cf-main">
          {/* Editor */}
          <div
            className="cf-editor-wrap"
            style={{ width: isExpanded ? "100%" : "62%" }}
          >
            <Editor
              height="100%"
              theme="vs-dark"
              language="python"
              value={pythonCode}
              onChange={(v) => setPythonCode(v || "")}
              options={{
                fontSize: 13.5,
                fontFamily: "'JetBrains Mono', monospace",
                fontLigatures: true,
                minimap: { enabled: false },
                automaticLayout: true,
                padding: { top: 16, bottom: 16 },
                scrollBeyondLastLine: false,
                cursorBlinking: "phase",
                cursorSmoothCaretAnimation: "on",
                smoothScrolling: true,
                bracketPairColorization: { enabled: true },
                lineNumbersMinChars: 3,
                renderLineHighlight: "gutter",
                glyphMargin: false,
                wordWrap: "on",
                overviewRulerLanes: 0,
                hideCursorInOverviewRuler: true,
                scrollbar: {
                  verticalScrollbarSize: 6,
                  horizontalScrollbarSize: 6,
                },
                lineHeight: 22,
              }}
            />
            {isRunning && <div className="cf-run-indicator" />}
          </div>

          {/* Output */}
          {!isExpanded && (
            <div className="cf-output-wrap" style={{ width: "38%" }}>
              <div className="cf-output-header">
                <div className="cf-output-title">
                  output
                  {runCount > 0 && !isRunning && (
                    <span className={`cf-badge ${hasError ? "err" : "ok"}`}>
                      {hasError ? "error" : "pass"}
                    </span>
                  )}
                </div>
                <button
                  className="cf-icon-btn"
                  onClick={() => { setOutput(""); setHasError(false); }}
                  title="clear"
                  style={{ fontSize: 12 }}
                >
                  ✕
                </button>
              </div>

              <div className="cf-output-body">
                <pre className={
                  hasError ? "error" : output ? "" : "empty"
                }>
                  {output || "waiting for input..."}
                </pre>
              </div>
            </div>
          )}
        </div>

        {/* ===== STATUS BAR ===== */}
        <div className="cf-statusbar">
          <div className="left">
            <span>python 3.11</span>
            <span>utf-8</span>
            <span>spaces: 4</span>
          </div>
          <div className="right">
            <span>ctrl+enter</span>
            <span className={isPythonReady ? "connected" : "disconnected"}>
              ● {isPythonReady ? "ready" : "offline"}
            </span>
          </div>
        </div>
      </div>
    </>
  );
};

export default CodeEditor;