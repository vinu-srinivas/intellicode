from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from app.analyzer.analyzer import analyze_code

from app.knowledge_base import (
    get_problem_by_id,
    load_problems,
    public_problem_details,
    public_problem_summary,
)


app = FastAPI(
    title="IntelliCode API",
    description="Backend API for the IntelliCode DSA learning assistant.",
    version="0.2.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to IntelliCode API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "IntelliCode API",
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
            if problem["difficulty"].casefold()
            == difficulty.casefold()
        ]

    if category:
        problems = [
            problem
            for problem in problems
            if category.casefold()
            in problem["category"].casefold()
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


@app.post("/analyze")
def analyze(request: CodeAnalysisRequest):

    if request.language.lower() != "python":
        raise HTTPException(
            status_code=400,
            detail="Only Python is supported currently."
        )

    result = analyze_code(request.code)

    return result