from app.analyzer.parser import parse_code
from app.analyzer.feature_extractor import FeatureExtractor
from app.analyzer.pattern_matcher import match_pattern
from app.analyzer.complexity_estimator import estimate_complexity
from app.analyzer.hint_generator import generate_hint
from app.analyzer.multi_lang_analyzer import analyze_c_style_code
from app.knowledge_base import get_problem_by_id


def analyze_code(
    code: str,
    problem_id: int | None = None,
    hint_level: int = 1,
    language: str = "python",
):
    """
    Execute full deterministic analysis pipeline for Python, Java, or C++:
    1. For Java / C++: analyze_c_style_code
    2. For Python: AST parsing + FeatureExtractor + PatternMatcher + ComplexityEstimator
    """
    lang = language.lower() if language else "python"

    if lang in {"java", "cpp", "c++"}:
        return analyze_c_style_code(
            code=code,
            language="cpp" if lang in {"cpp", "c++"} else "java",
            problem_id=problem_id,
            hint_level=hint_level,
        )

    parsed = parse_code(code)

    if not parsed["syntax_valid"]:
        return {
            "syntax_valid": False,
            "features": None,
            "pattern": None,
            "complexity": None,
            "hints": None,
            "hint": None,
            "problem_info": None,
            "error": parsed["error"],
        }

    tree = parsed["tree"]

    extractor = FeatureExtractor(source_code=code)
    extractor.visit(tree)
    features = extractor.get_features()

    problem = get_problem_by_id(problem_id) if problem_id else None
    target_complexity = (
        problem["primary_solution"]["complexity"] if problem and "primary_solution" in problem else None
    )

    match = match_pattern(features, code, problem_id)
    pattern_result = {
        "name": match.pattern,
        "display_name": match.display_name,
        "confidence": match.confidence,
        "evidence": match.evidence,
        "alternative": match.alternative,
        "is_optimal": match.is_optimal,
        "matched_approach_name": match.matched_approach_name,
    }

    complexity_result = estimate_complexity(
        code=code,
        features=features,
        target_complexity=target_complexity,
    )

    hints = {
        1: generate_hint(problem_id, match.pattern, 1),
        2: generate_hint(problem_id, match.pattern, 2),
        3: generate_hint(problem_id, match.pattern, 3),
    }

    current_hint = hints.get(hint_level, hints[1])

    problem_info = None
    if problem:
        problem_info = {
            "leetcode_id": problem["leetcode_id"],
            "title": problem["title"],
            "difficulty": problem["difficulty"],
            "category": problem["category"],
            "optimal_approach": problem["primary_solution"]["approach"],
            "optimal_complexity": problem["primary_solution"]["complexity"],
        }

    return {
        "syntax_valid": True,
        "features": features,
        "pattern": pattern_result,
        "complexity": complexity_result,
        "hints": hints,
        "hint": current_hint,
        "problem_info": problem_info,
        "error": None,
    }