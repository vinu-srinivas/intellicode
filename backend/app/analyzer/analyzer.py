from app.analyzer.parser import parse_code
from app.analyzer.feature_extractor import FeatureExtractor
from app.analyzer.pattern_matcher import match_two_sum
from app.analyzer.complexity_estimator import estimate_complexity


def analyze_code(code: str, problem_id: int | None = None):

    parsed = parse_code(code)

    if not parsed["syntax_valid"]:
        return {
            "syntax_valid": False,
            "features": None,
            "pattern": None,
            "complexity": None,
            "error": parsed["error"],
        }

    tree = parsed["tree"]

    extractor = FeatureExtractor()
    extractor.visit(tree)

    features = extractor.get_features()

    pattern_result = None

    if problem_id == 1:
        match = match_two_sum(features, code)

        pattern_result = {
            "name": match.pattern,
            "confidence": match.confidence,
            "evidence": match.evidence,
            "alternative": match.alternative,
        }

    complexity_result = estimate_complexity(code)

    return {
        "syntax_valid": True,
        "features": features,
        "pattern": pattern_result,
        "complexity": complexity_result,
        "error": None,
    }