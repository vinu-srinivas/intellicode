from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.analyzer.analyzer import analyze_code
from app.knowledge_base import (
    get_problem_by_id,
    load_problems,
    public_problem_details,
    public_problem_summary,
)
from app.runner import run_code_tests


app = FastAPI(
    title="SCRS API",
    description="Deterministic Static Analysis & Code Review for DSA Practice in Python, Java, and C++.",
    version="1.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to SCRS API",
        "system": "SCRS Code Review System for Curated DSA Practice",
        "status": "running",
        "version": "1.1.0",
        "supported_languages": ["python", "java", "cpp"],
        "mode": "deterministic_offline_non_llm",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SCRS API",
    }


@app.get("/problems")
def list_problems(
    difficulty: str | None = Query(
        default=None,
        description="Filter by difficulty: Easy, Medium, or Hard.",
    ),
    category: str | None = Query(
        default=None,
        description="Filter by problem category.",
    ),
    pattern: str | None = Query(
        default=None,
        description="Filter by algorithmic pattern.",
    ),
    q: str | None = Query(
        default=None,
        min_length=1,
        description="Search problem titles.",
    ),
):
    problems = load_problems()

    if difficulty:
        problems = [
            problem
            for problem in problems
            if problem["difficulty"].casefold() == difficulty.casefold()
        ]

    if category:
        problems = [
            problem
            for problem in problems
            if category.casefold() in problem["category"].casefold()
        ]

    if pattern:
        problems = [
            problem
            for problem in problems
            if any(
                pattern.casefold() in item.casefold()
                for item in problem["patterns"]
            )
        ]

    if q:
        search_term = q.casefold()
        problems = [
            problem
            for problem in problems
            if search_term in problem["title"].casefold()
        ]

    return {
        "total": len(problems),
        "problems": [
            public_problem_summary(problem)
            for problem in problems
        ],
    }


@app.get("/problems/{leetcode_id}")
def get_problem(leetcode_id: int):
    problem = get_problem_by_id(leetcode_id)

    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem not found.",
        )

    return public_problem_details(problem)


@app.get("/problems/{leetcode_id}/approaches")
def get_problem_approaches(leetcode_id: int):
    problem = get_problem_by_id(leetcode_id)

    if problem is None:
        raise HTTPException(
            status_code=404,
            detail="Problem not found.",
        )

    details = public_problem_details(problem)

    return {
        "leetcode_id": problem["leetcode_id"],
        "title": problem["title"],
        "approaches": details["approaches"],
        "primary_approach": details["primary_approach"],
        "primary_complexity": details["primary_complexity"],
    }


class CodeAnalysisRequest(BaseModel):
    code: str = Field(max_length=100_000)
    language: str = "python"
    problem_id: int | None = None
    hint_level: int = 1


@app.post("/analyze")
def analyze(request: CodeAnalysisRequest):
    lang = request.language.lower()
    if lang not in {"python", "java", "cpp", "c++"}:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language '{request.language}'. Supported: python, java, cpp.",
        )

    if request.problem_id is not None:
        problem = get_problem_by_id(request.problem_id)
        if problem is None:
            raise HTTPException(
                status_code=404,
                detail="Problem not found.",
            )

    result = analyze_code(
        code=request.code,
        problem_id=request.problem_id,
        hint_level=request.hint_level,
        language=lang,
    )

    return result


class CodeRunRequest(BaseModel):
    code: str = Field(max_length=100_000)
    problem_id: int | None = None
    language: str = "python"


@app.post("/run")
def run_code(request: CodeRunRequest):
    return run_code_tests(
        code=request.code,
        problem_id=request.problem_id,
        language=request.language,
    )


@app.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    """
    Real-time WebSocket endpoint for live debounced AST analysis
    during active code editing (Python, Java, and C++).
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            code = data.get("code", "")
            problem_id = data.get("problem_id")
            hint_level = data.get("hint_level", 1)
            language = data.get("language", "python")

            result = analyze_code(
                code=code,
                problem_id=problem_id,
                hint_level=hint_level,
                language=language,
            )
            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
    except Exception:
        try:
            await websocket.close()
        except Exception:
            pass