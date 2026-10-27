import ast
from dataclasses import dataclass


@dataclass
class DetectorResult:
    pattern: str
    confidence: str
    evidence: list[str]


class HashingDetector(ast.NodeVisitor):
    """Extract structural signals related to hashing."""

    def __init__(self):
        self.uses_dict = False
        self.uses_set = False
        self.uses_membership = False
        self.uses_frequency_update = False
        self.uses_dictionary_lookup = False
        self.uses_complement_expression = False

    def visit_Dict(self, node):
        self.uses_dict = True
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.uses_dict = True
        self.generic_visit(node)

    def visit_Set(self, node):
        self.uses_set = True
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self.uses_set = True
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == "dict":
                self.uses_dict = True
            elif node.func.id == "set":
                self.uses_set = True

        elif isinstance(node.func, ast.Attribute):
            method = node.func.attr

            if method == "get":
                self.uses_dictionary_lookup = True

            if method in {"add", "discard", "remove"}:
                self.uses_set = True

        self.generic_visit(node)

    def visit_Compare(self, node):
        for operator in node.ops:
            if isinstance(operator, (ast.In, ast.NotIn)):
                self.uses_membership = True

        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Examples: counts[key], seen[value]
        self.uses_dictionary_lookup = True
        self.generic_visit(node)

    def visit_BinOp(self, node):
        # A structural signal only; this is not enough by itself
        # to prove that the code implements complement lookup.
        if isinstance(node.op, (ast.Add, ast.Sub)):
            self.uses_complement_expression = True

        self.generic_visit(node)

    def visit_AugAssign(self, node):
        # Only treat indexed updates such as counts[key] += 1
        # as potential frequency-counting signals.
        if (
            isinstance(node.target, ast.Subscript)
            and isinstance(node.op, (ast.Add, ast.Sub))
        ):
            self.uses_frequency_update = True

        self.generic_visit(node)

    def get_features(self):
        return {
            "uses_dict": self.uses_dict,
            "uses_set": self.uses_set,
            "uses_membership": self.uses_membership,
            "uses_frequency_update": self.uses_frequency_update,
            "uses_dictionary_lookup": self.uses_dictionary_lookup,
            "uses_complement_expression": self.uses_complement_expression,
        }


def detect_hashing_pattern(code: str) -> DetectorResult:
    """Detect common hashing-related structural patterns."""

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return DetectorResult(
            pattern="unknown",
            confidence="low",
            evidence=["Code contains invalid Python syntax."],
        )

    detector = HashingDetector()
    detector.visit(tree)

    features = detector.get_features()
    evidence = []

    if features["uses_dict"]:
        evidence.append("Dictionary construction detected.")

    if features["uses_set"]:
        evidence.append("Set construction or set operations detected.")

    if features["uses_membership"]:
        evidence.append("Membership testing detected.")

    if features["uses_dictionary_lookup"]:
        evidence.append("Dictionary-style lookup detected.")

    if features["uses_frequency_update"]:
        evidence.append("Arithmetic update detected.")

    if not evidence:
        return DetectorResult(
            pattern="unknown",
            confidence="low",
            evidence=[
                "No strong hashing-related structural signals were found."
            ],
        )

    if (
        features["uses_dict"]
        and features["uses_complement_expression"]
    ):
        return DetectorResult(
            pattern="hash_map",
            confidence="medium",
            evidence=evidence + [
                "Dictionary usage and arithmetic expression detected."
            ],
        )

    if features["uses_set"] and features["uses_membership"]:
        return DetectorResult(
            pattern="hash_set",
            confidence="medium",
            evidence=evidence,
        )

    if (
        features["uses_dict"]
        and features["uses_frequency_update"]
    ):
        return DetectorResult(
            pattern="frequency_count",
            confidence="medium",
            evidence=evidence,
        )

    return DetectorResult(
        pattern="hashing",
        confidence="low",
        evidence=evidence,
    )