import ast


class FeatureExtractor(ast.NodeVisitor):

    def __init__(self):
        self.function_count = 0
        self.loop_count = 0
        self.max_loop_nesting = 0

        self.current_loop_depth = 0

        self.recursive_call_count = 0

        self.uses_dictionary = False
        self.uses_set = False
        self.uses_sorting = False

        self.function_stack = []

    def visit_FunctionDef(self, node):
        self.function_count += 1

        self.function_stack.append(node.name)

        self.generic_visit(node)

        self.function_stack.pop()

    def visit_AsyncFunctionDef(self, node):
        self.function_count += 1

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

        self.current_loop_depth += 1

        self.max_loop_nesting = max(
            self.max_loop_nesting,
            self.current_loop_depth
        )

        self.generic_visit(node)

        self.current_loop_depth -= 1

    def visit_Dict(self, node):
        self.uses_dictionary = True
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.uses_dictionary = True
        self.generic_visit(node)

    def visit_Set(self, node):
        self.uses_set = True
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self.uses_set = True
        self.generic_visit(node)

    def visit_Call(self, node):

        if isinstance(node.func, ast.Name):

            function_name = node.func.id

            if function_name == "dict":
                self.uses_dictionary = True

            if function_name == "set":
                self.uses_set = True

            if function_name == "sorted":
                self.uses_sorting = True

            if (
                self.function_stack
                and function_name == self.function_stack[-1]
            ):
                self.recursive_call_count += 1

        elif isinstance(node.func, ast.Attribute):

            if node.func.attr == "sort":
                self.uses_sorting = True

        self.generic_visit(node)

    def get_features(self):

        return {
            "function_count": self.function_count,
            "loop_count": self.loop_count,
            "max_loop_nesting": self.max_loop_nesting,
            "recursive_call_count": self.recursive_call_count,
            "uses_dictionary": self.uses_dictionary,
            "uses_set": self.uses_set,
            "uses_sorting": self.uses_sorting
        }