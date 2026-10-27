import { useState, useEffect, useRef, useCallback } from "react";
import Editor from "@monaco-editor/react";
import {
  FiPlay, FiRotateCcw, FiHelpCircle, FiCheckCircle,
  FiAlertTriangle, FiXCircle, FiSearch, FiBookOpen, FiCheck,
  FiZap, FiClock, FiCopy, FiTerminal,
  FiChevronDown, FiChevronLeft, FiChevronRight, FiTrendingUp, FiCpu, FiUnlock,
  FiX
} from "react-icons/fi";
import { SiPython, SiCplusplus } from "react-icons/si";
import { FaJava } from "react-icons/fa";

const API_BASE = "http://127.0.0.1:8000";
const WS_URL   = "ws://127.0.0.1:8000/ws/analyze";

// Branding logo: brackets with center slash and intelligent core node
function Logo() {
  return (
    <svg width="24" height="24" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="28" height="28" rx="6" fill="#202020" stroke="#333333" strokeWidth="1" />
      <path
        d="M9 8L4 14L9 20"
        stroke="#ffa116"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M19 8L24 14L19 20"
        stroke="#ffa116"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M16 6L12 22"
        stroke="#ffffff"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <circle cx="14" cy="14" r="2.2" fill="#ffa116" />
    </svg>
  );
}

const LANG_META = {
  python: { label: "Python", ext: "py",   icon: SiPython,    color: "#3776ab" },
  java:   { label: "Java",   ext: "java", icon: FaJava,      color: "#ea2d2e" },
  cpp:    { label: "C++",    ext: "cpp",  icon: SiCplusplus, color: "#00599c" },
};

function DiffBadge({ difficulty, size = "md" }) {
  if (!difficulty) return null;
  const lower = difficulty.toLowerCase();
  const cls = lower === "easy" ? "diff-easy" : lower === "hard" ? "diff-hard" : "diff-medium";
  return (
    <span className={`diff-badge ${cls}${size === "sm" ? " diff-badge--sm" : ""}`}>
      {difficulty}
    </span>
  );
}

// Core DSA topics for filtering
const CORE_TOPICS = [
  "All",
  "Arrays",
  "Strings",
  "Two Pointers",
  "Sliding Window",
  "Stack",
  "Binary Search",
  "Linked List",
  "Trees",
  "Heap",
  "Graphs",
  "Dynamic Programming",
  "Backtracking"
];

function getDisplayTopic(category) {
  if (!category) return "";
  const cat = category.toLowerCase();
  if (cat.includes("tree") || cat.includes("bst")) return "Trees";
  if (cat.includes("graph")) return "Graphs";
  if (cat.includes("dynamic") || cat.includes("dp")) return "Dynamic Programming";
  if (cat.includes("stack")) return "Stack";
  if (cat.includes("linked")) return "Linked List";
  if (cat.includes("heap")) return "Heap";
  if (cat.includes("pointer")) return "Two Pointers";
  if (cat.includes("window")) return "Sliding Window";
  if (cat.includes("binary search")) return "Binary Search";
  if (cat.includes("string")) return "Strings";
  if (cat.includes("backtrack")) return "Backtracking";
  if (cat.includes("array") || cat.includes("matrix") || cat.includes("interval") || cat.includes("prefix") || cat.includes("hash")) return "Arrays";
  return category.split("&")[0].trim();
}

function matchesTopic(problemCategory, selectedTopic) {
  if (selectedTopic === "All") return true;
  return getDisplayTopic(problemCategory) === selectedTopic;
}

// Problem picker modal with search, topic, and difficulty filters
function ProblemPickerModal({
  isOpen,
  onClose,
  problems,
  selectedProblemId,
  onSelectProblem,
}) {
  const [query, setQuery] = useState("");
  const [selectedDifficulty, setSelectedDifficulty] = useState("All");
  const [selectedTopic, setSelectedTopic] = useState("All");
  const searchInputRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => searchInputRef.current?.focus(), 60);
      const handleKeyDown = (e) => {
        if (e.key === "Escape") onClose();
      };
      window.addEventListener("keydown", handleKeyDown);
      return () => window.removeEventListener("keydown", handleKeyDown);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const difficulties = ["All", "Easy", "Medium", "Hard"];

  const filtered = problems.filter((p) => {
    const q = query.trim().toLowerCase();
    const cleanTopic = getDisplayTopic(p.category).toLowerCase();
    const matchQuery =
      !q ||
      p.title.toLowerCase().includes(q) ||
      p.leetcode_id.toString().includes(q) ||
      cleanTopic.includes(q);
    const matchDiff =
      selectedDifficulty === "All" ||
      (p.difficulty && p.difficulty.toLowerCase() === selectedDifficulty.toLowerCase());
    const matchTopic = matchesTopic(p.category, selectedTopic);
    return matchQuery && matchDiff && matchTopic;
  });

  return (
    <div className="ic-modal-overlay" onClick={onClose}>
      <div className="ic-modal" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div className="ic-modal-header">
          <div className="ic-modal-title-wrap">
            <div className="ic-modal-title">
              <FiBookOpen style={{ color: "var(--diff-easy)" }} />
              <span>Select Problem</span>
            </div>
            <div className="ic-modal-sub">
              DSA Practice Problems
            </div>
          </div>
          <button className="ic-modal-close" onClick={onClose} title="Close window (Esc)">
            <FiX />
          </button>
        </div>

        {/* Search Row */}
        <div className="ic-modal-search-row">
          <div className="ic-modal-search-box">
            <FiSearch />
            <input
              ref={searchInputRef}
              type="text"
              className="ic-modal-search-input"
              placeholder="Search by title, number, or topic..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            {query && (
              <button
                onClick={() => setQuery("")}
                style={{ background: "none", border: "none", color: "var(--text-3)", cursor: "pointer", display: "flex" }}
              >
                <FiX />
              </button>
            )}
          </div>
        </div>

        {/* Filter Rows */}
        <div className="ic-modal-filters">
          {/* Difficulty row */}
          <div className="ic-filter-row">
            <span className="ic-filter-row-label">Difficulty:</span>
            <div className="ic-filter-chips">
              {difficulties.map((diff) => (
                <button
                  key={diff}
                  className={`ic-filter-chip chip-${diff.toLowerCase()}${selectedDifficulty === diff ? " active" : ""}`}
                  onClick={() => setSelectedDifficulty(diff)}
                >
                  {diff}
                </button>
              ))}
            </div>
          </div>

          {/* Topic / Category row */}
          <div className="ic-filter-row">
            <span className="ic-filter-row-label">Topic:</span>
            <div className="ic-filter-chips">
              {CORE_TOPICS.map((topic) => (
                <button
                  key={topic}
                  className={`ic-filter-chip${selectedTopic === topic ? " active" : ""}`}
                  onClick={() => setSelectedTopic(topic)}
                >
                  {topic}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Results Count & Table Header */}
        <div className="ic-modal-count-row">
          Showing {filtered.length} of {problems.length} problems
        </div>

        <div className="ic-modal-table-header">
          <span># &amp; Title</span>
          <span>Topic &bull; Difficulty</span>
        </div>

        {/* Scrollable Problem List */}
        <div className="ic-modal-list">
          {filtered.map((p) => {
            const isSelected = selectedProblemId === p.leetcode_id;
            return (
              <button
                key={p.leetcode_id}
                className={`ic-modal-item${isSelected ? " active" : ""}`}
                onClick={() => {
                  onSelectProblem(p.leetcode_id);
                  onClose();
                }}
              >
                <div className="ic-modal-item-left">
                  <span className="ic-modal-item-num">#{p.leetcode_id}</span>
                  <span className="ic-modal-item-title">{p.title}</span>
                </div>
                <div className="ic-modal-item-right">
                  {p.category && <span className="ic-modal-item-cat">{getDisplayTopic(p.category)}</span>}
                  <DiffBadge difficulty={p.difficulty} size="sm" />
                  {isSelected && <FiCheck style={{ color: "var(--diff-easy)", marginLeft: 4 }} />}
                </div>
              </button>
            );
          })}

          {filtered.length === 0 && (
            <div className="ic-modal-empty">
              No problems match your current search and filter criteria.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Locate optimal typing cursor spot in starter / template code
function findInsertionPosition(text, lang) {
  if (!text) return { lineNumber: 1, column: 1, selectLength: 0 };
  const lines = text.split("\n");

  // 1. In Python, look for line with 'pass'
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    const passIdx = l.indexOf("pass");
    if (passIdx !== -1 && l.trim() === "pass") {
      return { lineNumber: i + 1, column: passIdx + 1, selectLength: 4 };
    }
  }

  // 2. Look for comment '// Write your solution here' or '# Write your solution here'
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (l.includes("Write your solution here") || l.includes("TODO")) {
      return { lineNumber: i + 1, column: l.length + 1, selectLength: 0 };
    }
  }

  // 3. In Java / C++ starter templates with return statement
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    const retIdx = l.indexOf("return");
    if (retIdx !== -1 && (lines.length <= 15 || i > 2)) {
      return { lineNumber: i + 1, column: retIdx + 1, selectLength: 0 };
    }
  }

  // 4. Fallback: find primary method body
  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    if (
      trimmed.startsWith("def ") ||
      trimmed.startsWith("public ") ||
      (trimmed.includes("(") && trimmed.endsWith("{"))
    ) {
      if (i + 1 < lines.length) {
        const nextLine = lines[i + 1];
        const indentMatch = nextLine.match(/^\s*/);
        const col = indentMatch ? indentMatch[0].length + 1 : 9;
        return { lineNumber: i + 2, column: col, selectLength: 0 };
      }
    }
  }

  return { lineNumber: lines.length, column: 1, selectLength: 0 };
}

function setCursorAtInsertionPoint(editor, text, lang) {
  if (!editor || !text) return;
  setTimeout(() => {
    try {
      const pos = findInsertionPosition(text, lang);
      if (pos.selectLength > 0) {
        editor.setSelection({
          startLineNumber: pos.lineNumber,
          startColumn: pos.column,
          endLineNumber: pos.lineNumber,
          endColumn: pos.column + pos.selectLength,
        });
      } else {
        editor.setPosition({ lineNumber: pos.lineNumber, column: pos.column });
      }
      editor.revealPositionInCenterIfOutsideViewport({
        lineNumber: pos.lineNumber,
        column: pos.column,
      });
      editor.focus();
    } catch {
      // safe fallback
    }
  }, 60);
}

// Main code editor component
export default function CodeEditor() {
  const [problems,            setProblems]            = useState([]);
  const [selectedProblemId,   setSelectedProblemId]   = useState(1);
  const [problemDetails,      setProblemDetails]      = useState(null);
  const [isProblemModalOpen,  setIsProblemModalOpen]  = useState(false);
  const [selectedLanguage,    setSelectedLanguage]    = useState("python");
  const [code,                setCode]                = useState("");
  const [activePreset,        setActivePreset]        = useState("starter");

  // Code persistence cache: key is `${problemId}_${language}`
  const codeCacheRef = useRef({});

  const editorRef   = useRef(null);
  const wsRef       = useRef(null);
  const debounceRef = useRef(null);

  const [leftTab,             setLeftTab]             = useState("problem");
  const [bottomOpen,          setBottomOpen]          = useState(true);
  const [bottomTab,           setBottomTab]           = useState("tests");
  const [activeTestCaseIndex, setActiveTestCaseIndex] = useState(0);

  // Real-time AST analysis results
  const [analysis,          setAnalysis]          = useState(null);
  const [lastValidAnalysis, setLastValidAnalysis] = useState(null);

  const [testResults,   setTestResults]   = useState(null);
  const [isRunningTests,setIsRunningTests]= useState(false);

  const [unlockedHints, setUnlockedHints] = useState(new Set([1]));
  const [toast,         setToast]         = useState(null);

  const showToast = (message, type = "info") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  // Fetch problems list on mount with auto-retry
  useEffect(() => {
    let isMounted = true;
    const fetchList = () => {
      fetch(`${API_BASE}/problems`)
        .then((r) => r.json())
        .then((d) => {
          if (isMounted) setProblems(d.problems || []);
        })
        .catch(() => {
          if (isMounted) {
            setTimeout(() => {
              fetch(`${API_BASE}/problems`)
                .then((r) => r.json())
                .then((d) => {
                  if (isMounted) setProblems(d.problems || []);
                })
                .catch(() => showToast("Could not load problems list", "error"));
            }, 1000);
          }
        });
    };
    fetchList();
    return () => { isMounted = false; };
  }, []);

  // Fetch problem details whenever selectedProblemId changes
  useEffect(() => {
    let isMounted = true;
    const fetchDetail = () => {
      fetch(`${API_BASE}/problems/${selectedProblemId}`)
        .then((r) => r.json())
        .then((d) => {
          if (!isMounted) return;
          setProblemDetails(d);
          setUnlockedHints(new Set([1]));
          setTestResults(null);

          // Check if user has cached code for this problem and current language
          const cacheKey = `${selectedProblemId}_${selectedLanguage}`;
          const cachedCode = codeCacheRef.current[cacheKey];

          if (cachedCode !== undefined) {
            setCode(cachedCode);
            setActivePreset("custom");
            triggerAnalysis(cachedCode, selectedLanguage);
            setCursorAtInsertionPoint(editorRef.current, cachedCode, selectedLanguage);
          } else {
            const starter = d.starter_codes?.[selectedLanguage] || d.starter_code || "";
            setCode(starter);
            codeCacheRef.current[cacheKey] = starter;
            setActivePreset("starter");
            triggerAnalysis(starter, selectedLanguage);
            setCursorAtInsertionPoint(editorRef.current, starter, selectedLanguage);
          }
        })
        .catch(() => {
          if (isMounted) {
            setTimeout(() => {
              fetch(`${API_BASE}/problems/${selectedProblemId}`)
                .then((r) => r.json())
                .then((d) => {
                  if (!isMounted) return;
                  setProblemDetails(d);
                  setUnlockedHints(new Set([1]));
                  setTestResults(null);
                  const starter = d.starter_codes?.[selectedLanguage] || d.starter_code || "";
                  setCode(starter);
                  codeCacheRef.current[`${selectedProblemId}_${selectedLanguage}`] = starter;
                  setActivePreset("starter");
                  triggerAnalysis(starter, selectedLanguage);
                })
                .catch(() => showToast("Failed to load problem details", "error"));
            }, 1000);
          }
        });
    };
    fetchDetail();
    return () => { isMounted = false; };
  }, [selectedProblemId]);

  // WebSocket for real-time AST analysis
  useEffect(() => {
    let ws = null;
    let retryTimeout = null;

    const connect = () => {
      ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const result = data.type === "analysis_result" ? data.result : data;
          setAnalysis(result);
          if (result && result.syntax_valid) {
            setLastValidAnalysis(result);
          }
        } catch {
          // ignore parsing error
        }
      };
      ws.onclose = () => {
        retryTimeout = setTimeout(connect, 2500);
      };
      ws.onerror = () => ws.close();
    };

    connect();
    return () => {
      if (retryTimeout) clearTimeout(retryTimeout);
      if (ws) ws.close();
    };
  }, []);

  // Debounced AST analysis trigger (sends code to backend via WebSocket or POST fallback)
  const triggerAnalysis = useCallback((codeToAnalyze, lang = selectedLanguage) => {
    if (debounceRef.current) clearTimeout(debounceRef.current);

    debounceRef.current = setTimeout(() => {
      const payload = {
        code: codeToAnalyze,
        problem_id: selectedProblemId,
        language: lang,
        hint_level: 1,
      };

      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify(payload));
      } else {
        fetch(`${API_BASE}/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        })
          .then((r) => r.json())
          .then((d) => {
            setAnalysis(d);
            if (d && d.syntax_valid) {
              setLastValidAnalysis(d);
            }
          })
          .catch(() => {});
      }
    }, 200);
  }, [selectedProblemId, selectedLanguage]);

  // Handle editor text change
  const handleEditorChange = (v) => {
    const val = v || "";
    setCode(val);
    codeCacheRef.current[`${selectedProblemId}_${selectedLanguage}`] = val;
    setActivePreset("custom");
    triggerAnalysis(val, selectedLanguage);
  };

  // Switch language while preserving user's code for each language
  const handleLanguageChange = (nextLang) => {
    if (nextLang === selectedLanguage) return;

    // 1. Save current code in cache
    codeCacheRef.current[`${selectedProblemId}_${selectedLanguage}`] = code;

    // 2. Set new language
    setSelectedLanguage(nextLang);

    // 3. Check if cached code exists for nextLang on this problem
    const cacheKey = `${selectedProblemId}_${nextLang}`;
    const cached = codeCacheRef.current[cacheKey];

    if (cached !== undefined && cached.trim().length > 0) {
      setCode(cached);
      setActivePreset("custom");
      triggerAnalysis(cached, nextLang);
      setCursorAtInsertionPoint(editorRef.current, cached, nextLang);
      showToast(`Switched to ${LANG_META[nextLang].label} (restored code)`);
    } else {
      const starter = problemDetails?.starter_codes?.[nextLang] || "";
      setCode(starter);
      codeCacheRef.current[cacheKey] = starter;
      setActivePreset("starter");
      triggerAnalysis(starter, nextLang);
      setCursorAtInsertionPoint(editorRef.current, starter, nextLang);
      showToast(`Switched to ${LANG_META[nextLang].label}`);
    }
  };

  // Handle preset demo load
  const handleSelectPreset = (preset) => {
    setActivePreset(preset);
    if (!problemDetails) return;

    if (preset === "starter") {
      const s = problemDetails.starter_codes?.[selectedLanguage] || problemDetails.starter_code || "";
      setCode(s);
      codeCacheRef.current[`${selectedProblemId}_${selectedLanguage}`] = s;
      triggerAnalysis(s, selectedLanguage);
      setCursorAtInsertionPoint(editorRef.current, s, selectedLanguage);
      showToast("Loaded starter template");
      return;
    }

    const approaches = problemDetails.approaches || [];
    let target;
    if (preset === "brute") {
      target =
        approaches.find((a) =>
          a.name.toLowerCase().includes("brute") || a.name.toLowerCase().includes("naive")
        ) || approaches[0];
    } else {
      target =
        approaches.find((a) =>
          a.name.toLowerCase().includes("optimal") || a.name === problemDetails.primary_approach
        ) || approaches[approaches.length - 1];

      // Ensure distinct preset if multiple approaches exist
      const bruteTarget = approaches.find((a) =>
        a.name.toLowerCase().includes("brute") || a.name.toLowerCase().includes("naive")
      ) || approaches[0];

      if (target === bruteTarget && approaches.length > 1) {
        target = approaches.find((a) => a !== bruteTarget) || approaches[1];
      }
    }

    if (!target) {
      showToast("No approaches available for this problem", "warn");
      return;
    }

    const src =
      target.code?.[selectedLanguage] ||
      target.code?.["python"] ||
      "";

    if (src) {
      setCode(src);
      codeCacheRef.current[`${selectedProblemId}_${selectedLanguage}`] = src;
      triggerAnalysis(src, selectedLanguage);
      setCursorAtInsertionPoint(editorRef.current, src, selectedLanguage);
      const label = preset === "brute" ? "Brute Force" : "Optimal";
      showToast(`${label} - ${target.name} loaded (${LANG_META[selectedLanguage].label})`);
    } else {
      showToast(`No ${LANG_META[selectedLanguage].label} code available for this approach`, "warn");
    }
  };

  const handleUnlockHint = (level) => {
    setUnlockedHints((prev) => new Set([...prev, level]));
    showToast(`Hint ${level} unlocked`, "success");
  };

  // Run tests (Python, Java, or C++)
  const handleRunTests = () => {
    setIsRunningTests(true);
    setBottomOpen(true);
    setBottomTab("tests");

    fetch(`${API_BASE}/run`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code,
        problem_id: selectedProblemId,
        language: selectedLanguage,
      }),
    })
      .then((r) => r.json())
      .then((d) => {
        setTestResults(d);
        setIsRunningTests(false);
        setActiveTestCaseIndex(0);
        showToast(
          d.success ? "All tests passed!" : "Some tests failed.",
          d.success ? "success" : "error"
        );
      })
      .catch(() => {
        setIsRunningTests(false);
        showToast("Execution error from test runner", "error");
      });
  };

  // Ref to always hold the latest handleRunTests function
  const runTestsRef = useRef(handleRunTests);
  useEffect(() => {
    runTestsRef.current = handleRunTests;
  });

  // Global keyboard shortcuts (Ctrl+Enter to run, Ctrl+K to open problems modal)
  useEffect(() => {
    const handleKey = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        e.stopPropagation();
        if (runTestsRef.current) {
          runTestsRef.current();
        }
      } else if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) {
        e.preventDefault();
        e.stopPropagation();
        setIsProblemModalOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKey, true);
    return () => window.removeEventListener("keydown", handleKey, true);
  }, []);

  const editorLanguage =
    selectedLanguage === "cpp"
      ? "cpp"
      : selectedLanguage === "java"
      ? "java"
      : "python";

  // Use active valid analysis if current syntax is mid-edit
  const activeAnalysis = (analysis && analysis.syntax_valid) ? analysis : (lastValidAnalysis || analysis);

  const currentIndex = problems.findIndex((p) => p.leetcode_id === selectedProblemId);
  const handlePrevProblem = () => {
    if (currentIndex > 0) {
      setSelectedProblemId(problems[currentIndex - 1].leetcode_id);
      setLeftTab("problem");
    }
  };
  const handleNextProblem = () => {
    if (currentIndex >= 0 && currentIndex < problems.length - 1) {
      setSelectedProblemId(problems[currentIndex + 1].leetcode_id);
      setLeftTab("problem");
    }
  };

  return (
    <div className="ic-root">
      {/* Toast Notification */}
      {toast && (
        <div className={`ic-toast ic-toast--${toast.type || "info"}`}>
          <span className="ic-toast-dot" />
          <span>{toast.message}</span>
        </div>
      )}

      {/* Problem Picker Modal Window */}
      <ProblemPickerModal
        isOpen={isProblemModalOpen}
        onClose={() => setIsProblemModalOpen(false)}
        problems={problems}
        selectedProblemId={selectedProblemId}
        onSelectProblem={(id) => {
          setSelectedProblemId(id);
          setLeftTab("problem");
        }}
      />

      {/* TOP NAVBAR */}
      <header className="ic-nav">
        {/* Left: Brand + Problem Window Trigger */}
        <div className="ic-nav-left">
          <div className="ic-brand">
            <div className="ic-brand-icon">
              <Logo />
            </div>
            <span className="ic-brand-name">SCRS</span>
          </div>

          <div className="ic-nav-sep" />

          {/* Quick Problem Prev/Next Nav and Trigger */}
          <div className="ic-problem-nav-group">
            <button
              className="ic-icon-nav-btn"
              onClick={handlePrevProblem}
              disabled={currentIndex <= 0}
              title="Previous Problem"
            >
              <FiChevronLeft />
            </button>
            <button
              className="ic-picker-btn"
              onClick={() => setIsProblemModalOpen(true)}
              title="Open Problem Search & Filter Window (Ctrl+K or click)"
            >
              <FiBookOpen className="ic-picker-icon" />
              <span className="ic-picker-num">{selectedProblemId}.</span>
              <span className="ic-picker-title">
                {problemDetails?.title || "Select Problem..."}
              </span>
              <DiffBadge difficulty={problemDetails?.difficulty} />
              <FiChevronDown style={{ color: "var(--text-3)", fontSize: 12, marginLeft: 2 }} />
            </button>
            <button
              className="ic-icon-nav-btn"
              onClick={handleNextProblem}
              disabled={currentIndex < 0 || currentIndex >= problems.length - 1}
              title="Next Problem"
            >
              <FiChevronRight />
            </button>
          </div>
        </div>

        {/* Center: Language Switcher with Official Logos */}
        <div className="ic-nav-center">
          <div className="ic-lang-group">
            {Object.entries(LANG_META).map(([id, meta]) => {
              const LangIcon = meta.icon;
              const isActive = selectedLanguage === id;
              return (
                <button
                  key={id}
                  onClick={() => handleLanguageChange(id)}
                  className={`ic-lang-btn${isActive ? " active" : ""}`}
                  title={`Switch to ${meta.label}`}
                >
                  <LangIcon
                    className="ic-lang-icon"
                    style={{
                      fontSize: 13,
                      color: isActive ? meta.color : "inherit",
                    }}
                  />
                  <span>{meta.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right: Demo Presets + Run Tests */}
        <div className="ic-nav-right">
          <div className="ic-demo-group">
            <button
              onClick={() => handleSelectPreset("starter")}
              className={`ic-demo-btn${activePreset === "starter" ? " active-starter" : ""}`}
              title="Reset to starter solution template"
            >
              <FiRotateCcw />
              Starter
            </button>
            <button
              onClick={() => handleSelectPreset("brute")}
              className={`ic-demo-btn${activePreset === "brute" ? " active-brute" : ""}`}
              title="Load Brute Force solution"
            >
              <FiTrendingUp />
              Brute Force
            </button>
            <button
              onClick={() => handleSelectPreset("optimal")}
              className={`ic-demo-btn${activePreset === "optimal" ? " active-optimal" : ""}`}
              title="Load Optimal solution"
            >
              <FiZap />
              Optimal
            </button>
          </div>

          <div className="ic-nav-sep" />

          <button
            onClick={handleRunTests}
            disabled={isRunningTests}
            className="ic-run-btn"
            title="Run code against test cases (Ctrl+Enter)"
          >
            {isRunningTests ? (
              <>
                <span className="ic-spinner" />
                <span>Running...</span>
              </>
            ) : (
              <>
                <FiPlay />
                <span>Run</span>
              </>
            )}
          </button>
        </div>
      </header>

      {/* MAIN TWO-PANE WORKSPACE */}
      <div className="ic-workspace">
        {/* LEFT COLUMN: Problem Details / Review / Hints */}
        <aside className="ic-left">
          <div className="ic-tab-bar">
            <button
              onClick={() => setLeftTab("problem")}
              className={`ic-tab${leftTab === "problem" ? " active" : ""}`}
            >
              <FiBookOpen />
              Description
            </button>
            <button
              onClick={() => setLeftTab("review")}
              className={`ic-tab${leftTab === "review" ? " active" : ""}`}
            >
              <FiCpu />
              Code Review
            </button>
            <button
              onClick={() => setLeftTab("hints")}
              className={`ic-tab${leftTab === "hints" ? " active" : ""}`}
            >
              <FiHelpCircle />
              Hints ({unlockedHints.size}/3)
            </button>
          </div>

          <div className="ic-left-body">
            {/* 1. CODE REVIEW TAB */}
            {leftTab === "review" && (
              <div className="ic-review">
                {/* Syntax Error Banner - only shown when invalid syntax is detected */}
                {analysis?.syntax_valid === false && (
                  <div className="ic-banner ic-banner--error">
                    <FiAlertTriangle style={{ fontSize: 16, flexShrink: 0 }} />
                    <div>
                      <div className="ic-banner-title">
                        {selectedLanguage.toUpperCase()} - Syntax Error
                      </div>
                      <div className="ic-banner-sub">
                        {typeof analysis.error === "object" && analysis.error
                          ? `Line ${analysis.error.line || 1}: ${analysis.error.message}`
                          : (analysis.error || "Incomplete statement while editing. Finish statement for AST update.")}
                      </div>
                    </div>
                  </div>
                )}

                {/* Algorithmic Pattern Card */}
                <div className="ic-card">
                  <div className="ic-card-header">
                    <span className="ic-card-label">Algorithmic Pattern</span>
                    <span className={`ic-badge ${activeAnalysis?.pattern?.is_optimal ? "ic-badge--green" : "ic-badge--amber"}`}>
                      {activeAnalysis?.pattern?.display_name || "Drafting Solution"}
                    </span>
                  </div>
                  <div className="ic-strategy-name">
                    {activeAnalysis?.pattern?.display_name || "In-Progress / Drafting Solution"}
                  </div>
                  {activeAnalysis?.pattern?.evidence?.length > 0 ? (
                    <ul style={{ margin: "8px 0 0", paddingLeft: 18, fontSize: 12, color: "var(--text-2)", lineHeight: 1.55 }}>
                      {activeAnalysis.pattern.evidence.map((ev, i) => (
                        <li key={i}>{ev}</li>
                      ))}
                    </ul>
                  ) : (
                    <p style={{ fontSize: 12.5, color: "var(--text-2)", marginTop: 6, lineHeight: 1.55 }}>
                      Write or paste code in the editor to instantly analyze its design pattern, loops, and data structures.
                    </p>
                  )}
                  {activeAnalysis?.pattern?.alternative && !activeAnalysis?.pattern?.is_optimal && (
                    <div className="ic-tip" style={{ marginTop: 10 }}>
                      <FiZap className="ic-tip-icon" />
                      <span>
                        Recommended alternative: <strong>{activeAnalysis.pattern.alternative}</strong>
                      </span>
                    </div>
                  )}
                </div>

                {/* Time & Space Complexity Card */}
                <div className="ic-card">
                  <div className="ic-card-header">
                    <span className="ic-card-label">Complexity Analysis</span>
                    {activeAnalysis?.complexity && (
                      <span className={`ic-badge ${activeAnalysis.pattern?.is_optimal || activeAnalysis.complexity.time === (activeAnalysis.complexity.target_time || problemDetails?.primary_complexity?.time) ? "ic-badge--green" : "ic-badge--amber"}`}>
                        {activeAnalysis.complexity.efficiency_rating || (activeAnalysis.pattern?.is_optimal ? "Optimal Solution" : "Can Be Improved")}
                      </span>
                    )}
                  </div>
                  <div className="ic-complexity-grid">
                    <div className="ic-complexity-cell">
                      <span className="ic-structure-key">Time Complexity</span>
                      <div
                        className="ic-complexity-value"
                        style={{
                          color:
                            activeAnalysis?.complexity?.time && (activeAnalysis.complexity.target_time || problemDetails?.primary_complexity?.time) && activeAnalysis.complexity.time === (activeAnalysis.complexity.target_time || problemDetails?.primary_complexity?.time)
                              ? "var(--accent-green)"
                              : activeAnalysis?.complexity?.time
                              ? "var(--accent-amber)"
                              : "var(--text-4)",
                        }}
                      >
                        {activeAnalysis?.complexity?.time || "-"}
                      </div>
                      <div className="ic-complexity-target">
                        Goal: {activeAnalysis?.complexity?.target_time || problemDetails?.primary_complexity?.time || "O(n)"}
                      </div>
                      <div className="ic-complexity-desc">
                        {activeAnalysis?.complexity?.time === "O(n^2)"
                          ? "Slow - nested loops detected"
                          : activeAnalysis?.complexity?.time === "O(n)"
                          ? "Great - single linear traversal"
                          : activeAnalysis?.complexity?.time === "O(1)"
                          ? "Instant - constant time"
                          : "Calculated from AST loop nesting"}
                      </div>
                    </div>

                    <div className="ic-complexity-cell">
                      <span className="ic-structure-key">Space Complexity</span>
                      <div
                        className="ic-complexity-value"
                        style={{
                          color:
                            activeAnalysis?.complexity?.space && (activeAnalysis.complexity.target_space || problemDetails?.primary_complexity?.space) && (activeAnalysis.complexity.space === (activeAnalysis.complexity.target_space || problemDetails?.primary_complexity?.space) || activeAnalysis.complexity.space === "O(1)")
                              ? "var(--accent-green)"
                              : activeAnalysis?.complexity?.space
                              ? "var(--accent-amber)"
                              : "var(--text-4)",
                        }}
                      >
                        {activeAnalysis?.complexity?.space || "-"}
                      </div>
                      <div className="ic-complexity-target">
                        Goal: {activeAnalysis?.complexity?.target_space || problemDetails?.primary_complexity?.space || "O(1)"}
                      </div>
                      <div className="ic-complexity-desc">
                        {activeAnalysis?.complexity?.space === "O(1)"
                          ? "Constant - minimal auxiliary memory"
                          : activeAnalysis?.complexity?.space === "O(n)"
                          ? "Linear - allocates hash map/array"
                          : "Calculated from data allocations"}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Analysis Insights & Tips (positioned right below Complexity Analysis) */}
                {activeAnalysis?.complexity?.evidence?.length > 0 && (
                  <div className="ic-card">
                    <div className="ic-card-header">
                      <span className="ic-card-label">Analysis Insights</span>
                    </div>
                    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                      {activeAnalysis.complexity.evidence.map((ev, i) => (
                        <div key={i} className="ic-tip">
                          <FiZap className="ic-tip-icon" />
                          <span>{ev}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Code Structure Metrics (followed after Analysis Insights) */}
                <div className="ic-card">
                  <div className="ic-card-header">
                    <span className="ic-card-label">Structural Metrics</span>
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                    <div className="ic-structure-row">
                      <span className="ic-structure-key">Loop Count</span>
                      <span className="ic-structure-val">{activeAnalysis?.features?.loop_count ?? 0}</span>
                    </div>
                    <div className="ic-structure-row">
                      <span className="ic-structure-key">Max Loop Nesting Depth</span>
                      <span className="ic-structure-val">{activeAnalysis?.features?.max_loop_nesting ?? 0}</span>
                    </div>
                    <div className="ic-structure-row">
                      <span className="ic-structure-key">Hash Map / Set Usage</span>
                      <span className="ic-structure-val">
                        {(activeAnalysis?.features?.uses_dictionary || activeAnalysis?.features?.uses_set) ? "Yes (O(1) lookups)" : "No"}
                      </span>
                    </div>
                    <div className="ic-structure-row">
                      <span className="ic-structure-key">Recursion Detected</span>
                      <span className="ic-structure-val">
                        {activeAnalysis?.features?.has_recursion ? "Yes" : "No"}
                      </span>
                    </div>
                    <div className="ic-structure-row">
                      <span className="ic-structure-key">Two Pointers</span>
                      <span className="ic-structure-val">
                        {activeAnalysis?.features?.has_two_pointers ? "Yes" : "No"}
                      </span>
                    </div>
                    <div className="ic-structure-row">
                      <span className="ic-structure-key">Sorting Detected</span>
                      <span className="ic-structure-val">
                        {activeAnalysis?.features?.uses_sorting ? "Yes" : "No"}
                      </span>
                    </div>

                    {activeAnalysis?.features?.detected_data_structures?.length > 0 && (
                      <div style={{ marginTop: 6, paddingTop: 6, borderTop: "1px solid var(--border-1)" }}>
                        <span className="ic-structure-key" style={{ display: "block", marginBottom: 5 }}>Detected Collections:</span>
                        <div className="ic-ds-tags">
                          {activeAnalysis.features.detected_data_structures.map((ds, i) => (
                            <span key={i} className="ic-ds-tag">{ds}</span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* 2. PROBLEM DESCRIPTION TAB */}
            {leftTab === "problem" && (
              <div className="ic-problem-tab">
                <div className="ic-problem-heading">
                  <h1 className="ic-problem-title">
                    {problemDetails?.leetcode_id}. {problemDetails?.title}
                  </h1>
                </div>

                <div className="ic-problem-meta">
                  <DiffBadge difficulty={problemDetails?.difficulty} />
                  {problemDetails?.category && (
                    <span className="ic-tag ic-tag--blue">{getDisplayTopic(problemDetails.category)}</span>
                  )}
                </div>

                <div className="ic-problem-desc">
                  {problemDetails?.description || "Select a problem to view its statement."}
                </div>

                {/* Examples */}
                {problemDetails?.examples?.length > 0 && (
                  <div>
                    <div className="ic-section-label">Examples</div>
                    <div className="ic-examples">
                      {problemDetails.examples.map((ex, i) => (
                        <div key={i} className="ic-example">
                          <div className="ic-example-header">
                            Example {i + 1}:
                          </div>
                          <div className="ic-example-row">
                            <span className="ic-example-key">Input:</span>
                            <span className="ic-example-val">{ex.input}</span>
                          </div>
                          <div className="ic-example-row">
                            <span className="ic-example-key">Output:</span>
                            <span className="ic-example-val green">{ex.output}</span>
                          </div>
                          {ex.explanation && (
                            <div className="ic-example-explain">
                              <strong>Explanation:</strong> {ex.explanation}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Constraints */}
                {problemDetails?.constraints?.length > 0 && (
                  <div>
                    <div className="ic-section-label">Constraints</div>
                    <div className="ic-constraints">
                      {problemDetails.constraints.map((c, i) => (
                        <div key={i} className="ic-constraint-row">
                          <span className="ic-constraint-dot" />
                          <code>{c}</code>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* 3. STEP-BY-STEP HINTS TAB */}
            {leftTab === "hints" && (
              <div className="ic-hints-tab">
                <div style={{ fontSize: 12, color: "var(--text-3)", marginBottom: 4, lineHeight: 1.5 }}>
                  Hints guide your DSA problem solving systematically without giving away the answer upfront.
                </div>

                {[
                  { level: 1, title: "The Performance Bottleneck", sub: "Analyze what operations are repeated in the brute force approach" },
                  { level: 2, title: "Data Structure Selection",  sub: "Choose an optimal data structure to reduce lookup or traversal time" },
                  { level: 3, title: "Algorithm Blueprint",        sub: "Step-by-step logic and invariant rules for the final solution" },
                ].map(({ level, title, sub }) => {
                  const isUnlocked = unlockedHints.has(level);
                  const hintObj = problemDetails?.hints?.[level - 1] || activeAnalysis?.hints?.[level] || activeAnalysis?.hints?.[String(level)];
                  const hintText = typeof hintObj === "object" ? hintObj?.message : (hintObj || problemDetails?.hints?.[level - 1]);

                  return (
                    <div key={level} className={`ic-hint-card${isUnlocked ? " unlocked" : ""}`}>
                      <div className="ic-hint-header">
                        <div className="ic-hint-meta">
                          <div className={`ic-hint-num${isUnlocked ? " active" : ""}`}>
                            {level}
                          </div>
                          <div>
                            <div className="ic-hint-title">{title}</div>
                            <div className="ic-hint-sub">{sub}</div>
                          </div>
                        </div>
                        {isUnlocked ? (
                          <span className="ic-unlock-btn ic-unlock-btn--ready">
                            <FiCheck style={{ marginRight: 2, verticalAlign: -1 }} /> Ready
                          </span>
                        ) : (
                          <button
                            onClick={() => handleUnlockHint(level)}
                            className="ic-unlock-btn"
                          >
                            <FiUnlock /> Unlock
                          </button>
                        )}
                      </div>

                      {isUnlocked && (
                        <div className="ic-hint-body">
                          {hintText || "Analyze your loop bounds and see which calculations can be stored or looked up in O(1)."}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </aside>

        {/* RIGHT COLUMN: Monaco Editor + Bottom Test Results Drawer */}
        <main className="ic-editor-col">
          {/* Editor file tab bar */}
          <div className="ic-editor-tabbar">
            <div className="ic-editor-filetab">
              {(() => {
                const ActiveLangIcon = LANG_META[selectedLanguage]?.icon;
                return ActiveLangIcon ? (
                  <ActiveLangIcon style={{ color: LANG_META[selectedLanguage]?.color, fontSize: 13 }} />
                ) : (
                  <FiTerminal style={{ color: "var(--text-3)" }} />
                );
              })()}
              <span className="ic-filename">solution.{LANG_META[selectedLanguage].ext}</span>
            </div>
            <div className="ic-editor-actions">
              <button
                className="ic-icon-btn"
                onClick={() => {
                  navigator.clipboard.writeText(code);
                  showToast("Code copied to clipboard", "success");
                }}
                title="Copy code to clipboard"
              >
                <FiCopy />
              </button>
              <button
                className="ic-icon-btn"
                onClick={() => handleSelectPreset("starter")}
                title="Reset to starter template"
              >
                <FiRotateCcw />
              </button>
            </div>
          </div>

          {/* Monaco Editor Container */}
          <div className="ic-monaco-wrap">
            <Editor
              height="100%"
              language={editorLanguage}
              theme="vs-dark"
              value={code}
              onChange={handleEditorChange}
              onMount={(editor, monaco) => {
                editorRef.current = editor;

                // Remeasure fonts as soon as loaded so cursor aligns with pixel-perfect accuracy
                if (document.fonts) {
                  document.fonts.ready.then(() => {
                    monaco.editor.remeasureFonts();
                  });
                }

                // Bind Ctrl+Enter and Cmd+Enter directly inside Monaco editor
                editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
                  if (runTestsRef.current) {
                    runTestsRef.current();
                  }
                });

                // Set initial typing cursor to the exact spot in the method body and focus
                setCursorAtInsertionPoint(editor, code, selectedLanguage);
              }}
              options={{
                fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
                fontSize: 13.5,
                lineHeight: 22,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                renderLineHighlight: "all",
                cursorBlinking: "smooth",
                cursorStyle: "line",
                cursorWidth: 2,
                smoothScrolling: true,
                padding: { top: 12, bottom: 12 },
                bracketPairColorization: { enabled: true },
                automaticLayout: true,
                tabSize: 4,
                insertSpaces: true,
              }}
            />
          </div>

          {/* Bottom Drawer: Test Results & Terminal */}
          <div className={`ic-bottom ${bottomOpen ? "open" : "collapsed"}`}>
            <div
              className="ic-bottom-bar"
              onClick={() => {
                if (!bottomOpen) setBottomOpen(true);
              }}
              style={{ cursor: bottomOpen ? "default" : "pointer" }}
            >
              <div className="ic-bottom-tabs">
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setBottomTab("tests");
                    setBottomOpen(true);
                  }}
                  className={`ic-bottom-tab${bottomTab === "tests" ? " active" : ""}`}
                >
                  <FiTerminal />
                  Test Results
                  {testResults && (
                    <span className={`ic-badge-sm ${testResults.success ? "green" : "red"}`}>
                      {testResults.passed}/{testResults.total}
                    </span>
                  )}
                </button>
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                {testResults?.runtime_ms !== undefined && (
                  <span style={{ fontSize: 11, color: "var(--text-3)", fontFamily: "var(--font-mono)" }}>
                    <FiClock style={{ verticalAlign: -1, marginRight: 4 }} /> {testResults.runtime_ms} ms
                  </span>
                )}
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setBottomOpen((o) => !o);
                  }}
                  className="ic-bottom-toggle"
                  title={bottomOpen ? "Collapse drawer" : "Expand drawer"}
                  aria-label={bottomOpen ? "Collapse drawer" : "Expand drawer"}
                >
                  <FiChevronDown
                    style={{
                      transform: bottomOpen ? "none" : "rotate(180deg)",
                      transition: "transform 0.15s",
                      pointerEvents: "none"
                    }}
                  />
                </button>
              </div>
            </div>

            {bottomOpen && (
              <div className="ic-bottom-body">
                {isRunningTests ? (
                  <div style={{ display: "flex", alignItems: "center", gap: 10, color: "var(--text-2)", padding: "16px 0" }}>
                    <span className="ic-spinner" style={{ borderColor: "rgba(255,255,255,0.2)", borderTopColor: "var(--text-1)" }} />
                    <span>Compiling and executing tests in {LANG_META[selectedLanguage].label}...</span>
                  </div>
                ) : testResults ? (
                  <div className="ic-tests">
                    {/* Summary row */}
                    <div className="ic-tests-summary">
                      {testResults.success ? (
                        <div className="ic-result-ok">
                          <FiCheckCircle />
                          <span>Accepted</span>
                        </div>
                      ) : (
                        <div className="ic-result-fail">
                          <FiXCircle />
                          <span>{testResults.error ? "Runtime Error" : "Wrong Answer"}</span>
                        </div>
                      )}
                      <span style={{ fontSize: 11.5, color: "var(--text-3)", fontFamily: "var(--font-mono)" }}>
                        {testResults.passed}/{testResults.total} test cases passed &bull; Runtime: {testResults.runtime_ms} ms
                      </span>
                    </div>

                    {/* Test case tabs */}
                    {testResults.test_results?.length > 0 ? (
                      <>
                        <div className="ic-test-case-tabs">
                          {testResults.test_results.map((tc, idx) => (
                            <button
                              key={idx}
                              onClick={() => setActiveTestCaseIndex(idx)}
                              className={`ic-tc-tab${activeTestCaseIndex === idx ? " active" : ""}`}
                            >
                              <span className={`ic-tc-dot ${tc.passed ? "ok" : "fail"}`} />
                              Case {tc.case_number || idx + 1}
                            </button>
                          ))}
                        </div>

                        {testResults.test_results[activeTestCaseIndex] && (
                          <div className="ic-tc-detail">
                            <div className="ic-tc-row">
                              <div className="ic-tc-label">Input</div>
                              <div className="ic-tc-val">{testResults.test_results[activeTestCaseIndex].input}</div>
                            </div>
                            <div className="ic-tc-row">
                              <div className="ic-tc-label">Expected Output</div>
                              <div className="ic-tc-val ok">{testResults.test_results[activeTestCaseIndex].expected}</div>
                            </div>
                            <div className="ic-tc-row" style={{ gridColumn: "1 / -1" }}>
                              <div className="ic-tc-label">Actual Output</div>
                              <div className={`ic-tc-val ${testResults.test_results[activeTestCaseIndex].passed ? "ok" : "fail"}`}>
                                {testResults.test_results[activeTestCaseIndex].actual}
                              </div>
                            </div>
                            {testResults.test_results[activeTestCaseIndex].error && (
                              <div className="ic-tc-row" style={{ gridColumn: "1 / -1", borderColor: "rgba(239,68,68,0.3)" }}>
                                <div className="ic-tc-label" style={{ color: "var(--accent-red)" }}>Error Message</div>
                                <div className="ic-tc-val fail">{testResults.test_results[activeTestCaseIndex].error}</div>
                              </div>
                            )}
                          </div>
                        )}
                      </>
                    ) : (
                      <div style={{ color: "var(--text-3)", padding: 8 }}>
                        {testResults.success ? "Code executed cleanly without exceptions." : testResults.error}
                      </div>
                    )}
                  </div>
                ) : (
                  <div style={{ color: "var(--text-3)", padding: "12px 0", lineHeight: 1.6 }}>
                    Click <strong style={{ color: "var(--text-1)" }}>Run Tests</strong> (or press <strong style={{ color: "var(--text-1)" }}>Ctrl+Enter</strong>) to compile and evaluate your {LANG_META[selectedLanguage].label} code against sample test cases.
                  </div>
                )}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
