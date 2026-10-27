import ast
from app.analyzer.feature_extractor import FeatureExtractor


class ComplexityAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.loop_stack = []
        self.loop_count = 0
        self.max_loop_depth = 0

        self.has_sorting = False
        self.has_recursion = False

        self.constant_bound_loop_count = 0
        self.input_dependent_loop_count = 0

        self.function_stack = []
        self.recursive_call_count = 0

    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)
        self.generic_visit(node)
        self.function_stack.pop()

    def visit_AsyncFunctionDef(self, node):
        self.function_stack.append(node.name)
        self.generic_visit(node)
        self.function_stack.pop()

    def visit_For(self, node):
        self._visit_loop(node)

    def visit_AsyncFor(self, node):
        self._visit_loop(node)

    def visit_While(self, node):
        self._visit_loop(node)

    def _visit_loop(self, node):
        self.loop_count += 1

        loop_is_constant = self._is_constant_bound(node)

        if loop_is_constant:
            self.constant_bound_loop_count += 1
        else:
            self.input_dependent_loop_count += 1

        self.loop_stack.append(loop_is_constant)

        self.max_loop_depth = max(
            self.max_loop_depth,
            sum(not item for item in self.loop_stack),
        )

        self.generic_visit(node)
        self.loop_stack.pop()

    def _is_constant_bound(self, node):
        """
        Recognize a limited set of constant-bound loops.
        """
        if isinstance(node, (ast.For, ast.AsyncFor)):
            iterator = node.iter
            if (
                isinstance(iterator, ast.Call)
                and isinstance(iterator.func, ast.Name)
                and iterator.func.id == "range"
            ):
                return all(
                    isinstance(arg, ast.Constant)
                    and isinstance(arg.value, (int, float))
                    for arg in iterator.args
                )
        return False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == "sorted":
                self.has_sorting = True

            if (
                self.function_stack
                and (node.func.id == self.function_stack[-1] or node.func.id in {"dfs", "helper", "backtrack"})
            ):
                self.recursive_call_count += 1
                self.has_recursion = True

        elif isinstance(node.func, ast.Attribute):
            if node.func.attr == "sort":
                self.has_sorting = True

        self.generic_visit(node)

    def get_features(self):
        return {
            "loop_count": self.loop_count,
            "max_loop_depth": self.max_loop_depth,
            "constant_bound_loop_count": self.constant_bound_loop_count,
            "input_dependent_loop_count": self.input_dependent_loop_count,
            "has_sorting": self.has_sorting,
            "has_recursion": self.has_recursion,
            "recursive_call_count": self.recursive_call_count,
        }


def estimate_complexity(code: str, features: dict | None = None, target_complexity: dict | None = None):
    """
    Estimate time and auxiliary space complexity for AST structural patterns.
    Compare against target optimal complexity if provided.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {
            "status": "invalid_syntax",
            "time": "Unknown",
            "space": "Unknown",
            "evidence": [error.msg],
            "efficiency_rating": "Syntax Error",
        }

    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)
    c_features = analyzer.get_features()

    if features is None:
        extractor = FeatureExtractor(code)
        extractor.visit(tree)
        features = extractor.get_features()

    evidence = []
    estimated_time = "Unknown"
    estimated_space = "O(1)"
    status = "estimated"

    # Space estimation
    if (
        features.get("uses_dictionary")
        or features.get("uses_set")
        or features.get("uses_stack")
        or features.get("uses_deque")
        or features.get("has_dp_table")
    ):
        estimated_space = "O(n)"
        evidence.append("Uses an auxiliary data structure (hash map / set / stack) storing up to O(n) items.")
    elif features.get("uses_heap"):
        estimated_space = "O(k)"
        evidence.append("Uses a heap of size k to track extremal elements.")
    elif c_features["has_recursion"]:
        estimated_space = "O(n)"
        evidence.append("Function call stack grows with recursion depth (O(n) auxiliary stack memory).")
    else:
        estimated_space = "O(1)"
        evidence.append("Only uses a few pointers or scalar variables, keeping memory at O(1) minimal extra space.")

    # Time estimation
    if features.get("has_binary_search"):
        estimated_time = "O(log n)"
        evidence.append("Binary search pattern detected: cuts the search space in half each iteration (O(log n)).")

    elif c_features["has_recursion"]:
        if features.get("uses_dictionary") or features.get("has_dp_table"):
            estimated_time = "O(n)"
            evidence.append("Recursion with memoization/cache detected: avoids recalculating past states.")
        elif c_features["recursive_call_count"] >= 2:
            status = "unsupported_pattern"
            estimated_time = "O(2^n)"
            evidence.append("Branching recursion without memoization detected: branches exponentially (O(2^n)).")
        else:
            status = "unsupported_pattern"
            estimated_time = "Unknown"
            evidence.append("Recursive calls detected. Analyzing state transitions...")

    elif c_features["has_sorting"]:
        estimated_time = "O(n log n)"
        evidence.append("Built-in sort detected: standard comparison sort takes O(n log n) time.")

    elif features.get("has_sliding_window") or features.get("has_two_pointers"):
        estimated_time = "O(n)"
        if features.get("has_sliding_window"):
            evidence.append("Sliding window detected: each element enters and leaves the window at most once (O(n)).")
        else:
            evidence.append("Two-pointer scan detected: pointers meet in a single linear pass (O(n)).")

    elif c_features["loop_count"] == 0:
        estimated_time = "O(1)"
        evidence.append("No loops detected: runs in instant O(1) constant time.")

    elif c_features["input_dependent_loop_count"] == 0:
        estimated_time = "O(1)"
        evidence.append("Only constant-bound loops detected: runs in O(1) constant time.")

    elif c_features["max_loop_depth"] == 1:
        estimated_time = "O(n)"
        evidence.append("Single loop over input detected: runs in clean O(n) linear time.")

    elif c_features["max_loop_depth"] >= 2:
        depth = c_features["max_loop_depth"]
        estimated_time = f"O(n^{depth})" if depth > 1 else "O(n)"
        evidence.append(f"Found {depth} nested loops. Iterating through the input inside another loop takes O(n^{depth}) time.")

    # Efficiency rating compared to optimal target complexity
    efficiency_rating = "Analyzing"
    target_time = None
    target_space = None

    if target_complexity and isinstance(target_complexity, dict):
        target_time = target_complexity.get("time")
        target_space = target_complexity.get("space")

        # Canonical ranking: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n)
        order = {
            "O(1)": 1,
            "O(log n)": 2,
            "O(n)": 3,
            "O(n log n)": 4,
            "O(n^2)": 5,
            "O(n^3)": 6,
            "O(2^n)": 7,
        }

        est_rank = order.get(estimated_time, 99)
        tgt_rank = order.get(target_time, 99)

        if est_rank <= tgt_rank and estimated_time != "Unknown":
            efficiency_rating = "Optimal Time"
        elif est_rank > tgt_rank and estimated_time != "Unknown":
            if est_rank >= 5:
                efficiency_rating = "Suboptimal (Brute Force)"
            else:
                efficiency_rating = "Suboptimal Time"
        else:
            efficiency_rating = "Approaching Target"

    return {
        "status": status,
        "time": estimated_time,
        "space": estimated_space,
        "evidence": evidence,
        "target_time": target_time,
        "target_space": target_space,
        "efficiency_rating": efficiency_rating,
    }