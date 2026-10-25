import ast


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

        This is a conservative syntactic heuristic, not a
        complete proof of the loop's iteration count.
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
                and node.func.id == self.function_stack[-1]
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


def estimate_complexity(code: str):
    """
    Estimate time and auxiliary space complexity for supported
    structural patterns.

    Returns Unknown when the code does not fit a supported rule.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {
            "status": "invalid_syntax",
            "time": "Unknown",
            "space": "Unknown",
            "evidence": [error.msg],
        }

    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)

    features = analyzer.get_features()

    # Recursion is not yet analyzed with recurrence relations.
    if features["has_recursion"]:
        return {
            "status": "unsupported_pattern",
            "time": "Unknown",
            "space": "Unknown",
            "evidence": [
                "Recursive calls were detected.",
                "Recurrence analysis is not implemented yet.",
            ],
        }

    # Sorting is supported as a common time-complexity pattern.
    if features["has_sorting"]:
        return {
            "status": "estimated",
            "time": "O(n log n)",
            "space": "Implementation-dependent",
            "evidence": [
                "A standard sorting operation was detected.",
                "The estimate assumes comparison-based sorting.",
            ],
        }

    # No loops: do not assume arbitrary function calls are constant time.
    if features["loop_count"] == 0:
        return {
            "status": "estimated",
            "time": "O(1)",
            "space": "O(1)",
            "evidence": [
                "No loop structures were detected.",
                "This estimate assumes no input-dependent work "
                "inside function calls.",
            ],
        }

    # Only constant-bound loops.
    if features["input_dependent_loop_count"] == 0:
        return {
            "status": "estimated",
            "time": "O(1)",
            "space": "O(1)",
            "evidence": [
                "Only recognized constant-bound loops were detected."
            ],
        }

    # Sequential input-dependent loops.
    if features["max_loop_depth"] == 1:
        return {
            "status": "estimated",
            "time": "O(n)",
            "space": "O(1)",
            "evidence": [
                "Input-dependent loops have a maximum nesting depth of one."
            ],
        }

    # Nested input-dependent loops.
    depth = features["max_loop_depth"]

    return {
        "status": "estimated",
        "time": f"O(n^{depth})",
        "space": "O(1)",
        "evidence": [
            f"Maximum input-dependent loop nesting depth is {depth}.",
            "The estimate assumes each loop iterates O(n) times.",
            "The estimate assumes constant auxiliary storage.",
        ],
    }