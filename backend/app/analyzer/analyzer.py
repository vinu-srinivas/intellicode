from app.analyzer.parser import parse_code
from app.analyzer.feature_extractor import FeatureExtractor


def analyze_code(code: str):

    parsed = parse_code(code)

    if not parsed["syntax_valid"]:

        return {
            "syntax_valid": False,
            "features": None,
            "error": parsed["error"]
        }

    tree = parsed["tree"]

    extractor = FeatureExtractor()

    extractor.visit(tree)

    return {
        "syntax_valid": True,
        "features": extractor.get_features(),
        "error": None
    }