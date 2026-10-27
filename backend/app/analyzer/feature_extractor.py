import ast


class FeatureExtractor(ast.NodeVisitor):
    """
    Extract structural and algorithmic features from Python AST.
    Deterministic, rule-based feature extraction for DSA code.
    """

    def __init__(self, source_code: str = ""):
        self.source_code = source_code
        self.normalized_source = source_code.casefold()

        self.function_count = 0
        self.loop_count = 0
        self.max_loop_nesting = 0
        self.current_loop_depth = 0

        self.recursive_call_count = 0
        self.has_recursion = False

        self.uses_dictionary = False
        self.uses_set = False
        self.uses_sorting = False
        self.uses_heap = False
        self.uses_deque = False
        self.uses_stack = False

        self.function_stack = []

        # Pointer & Window signals
        self.pointer_initializations = set()
        self.has_converging_condition = False
        self.has_pointer_adjustment = False
        self.has_right_decrement = False
        self.has_window_contraction = False
        self.has_window_size_calc = False

        # Binary search signals
        self.has_mid_calc = False
        self.has_halving_update = False

        # Monotonic stack signals
        self.has_stack_monotonic_pop = False

        # Dynamic programming & Kadane signals
        self.has_kadane_pattern = False
        self.has_dp_table = False
        self.has_prefix_sum_pattern = False

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
        # Inspect while condition for pointer patterns
        self._inspect_while_condition(node.test)
        self._visit_loop(node)

    def _visit_loop(self, node):
        self.loop_count += 1
        self.current_loop_depth += 1
        self.max_loop_nesting = max(self.max_loop_nesting, self.current_loop_depth)

        # Check for monotonic stack pop: while stack and stack[-1] ...: stack.pop()
        if isinstance(node, ast.While):
            self._check_monotonic_while(node)

        self.generic_visit(node)
        self.current_loop_depth -= 1

    def _inspect_while_condition(self, test_node):
        """Check for pointer loop conditions like left < right, low <= high, l <= r."""
        if isinstance(test_node, ast.Compare):
            left_id = self._get_name_id(test_node.left)
            for comparator in test_node.comparators:
                right_id = self._get_name_id(comparator)
                if left_id and right_id:
                    pointer_pairs = {
                        ("left", "right"), ("l", "r"), ("low", "high"),
                        ("start", "end"), ("i", "j"), ("p1", "p2"),
                        ("slow", "fast"), ("head1", "head2")
                    }
                    if (left_id, right_id) in pointer_pairs or (right_id, left_id) in pointer_pairs:
                        self.has_converging_condition = True

    def _check_monotonic_while(self, node: ast.While):
        # Checks if condition references 'stack' and body contains stack.pop()
        cond_str = ast.unparse(node.test).lower() if hasattr(ast, "unparse") else ""
        if "stack" in cond_str:
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Attribute):
                    if stmt.func.attr == "pop":
                        self.has_stack_monotonic_pop = True

    def _get_name_id(self, node):
        if isinstance(node, ast.Name):
            return node.id.lower()
        return None

    def visit_Assign(self, node):
        # Check pointer assignments: left = 0, right = len(...) - 1, etc.
        for target in node.targets:
            target_name = self._get_name_id(target)
            if target_name in {"left", "right", "l", "r", "low", "high", "start", "end", "i", "j", "slow", "fast"}:
                self.pointer_initializations.add(target_name)

            # Check tuple unpack assignments: l, r = 0, len(nums) - 1
            if isinstance(target, ast.Tuple):
                for elt in target.elts:
                    elt_name = self._get_name_id(elt)
                    if elt_name in {"left", "right", "l", "r", "low", "high", "start", "end", "i", "j", "slow", "fast"}:
                        self.pointer_initializations.add(elt_name)

            # Check DP table assignments: dp = [0] * (n + 1) or dp = [[0]...]
            if target_name in {"dp", "memo", "cache", "table"}:
                self.has_dp_table = True

        # Check mid calculation: mid = (left + right) // 2 or (low + high) // 2
        assign_str = ast.unparse(node).lower() if hasattr(ast, "unparse") else ""
        if "mid" in assign_str and ("// 2" in assign_str or ">> 1" in assign_str):
            self.has_mid_calc = True

        # Check window size calculation: max_len = max(max_len, right - left + 1)
        if "right - left + 1" in assign_str or "right - left +1" in assign_str or "r - l + 1" in assign_str or "end - start + 1" in assign_str:
            self.has_window_size_calc = True

        self.generic_visit(node)

    def visit_AugAssign(self, node):
        # Check pointer movement: left += 1, right -= 1, etc.
        target_name = self._get_name_id(node.target)
        if target_name in {"left", "l", "start", "low", "slow"} and isinstance(node.op, ast.Add):
            self.has_pointer_adjustment = True
        elif target_name in {"right", "r", "end", "high"} and isinstance(node.op, ast.Sub):
            self.has_pointer_adjustment = True
            self.has_right_decrement = True
        elif target_name in {"i", "j"} and isinstance(node.op, (ast.Add, ast.Sub)):
            self.has_pointer_adjustment = True

        # Check window contraction: left += 1 inside an inner loop
        if self.current_loop_depth >= 2 and target_name in {"left", "l", "start"}:
            self.has_window_contraction = True

        self.generic_visit(node)

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
        func_name = ""
        attr_name = ""

        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr
            if isinstance(node.func.value, ast.Name):
                func_name = f"{node.func.value.id}.{attr_name}"

        # Dictionary detection
        if func_name in {"dict", "defaultdict", "Counter"}:
            self.uses_dictionary = True

        # Set detection
        if func_name == "set" or attr_name in {"add", "discard", "remove", "union", "intersection"}:
            self.uses_set = True

        # Sorting detection
        if func_name == "sorted" or attr_name == "sort":
            self.uses_sorting = True

        # Heap detection
        if "heapq" in func_name or attr_name in {"heappush", "heappop", "heapify", "nlargest", "nsmallest"}:
            self.uses_heap = True

        # Deque / Queue detection
        if func_name in {"deque", "collections.deque", "Queue"} or attr_name in {"popleft", "appendleft"}:
            self.uses_deque = True

        # Stack detection: list append and pop
        if attr_name == "pop":
            # If no args or arg is -1, it is LIFO stack pop
            if not node.args or (isinstance(node.args[0], ast.UnaryOp) and isinstance(node.args[0].operand, ast.Constant) and node.args[0].operand.value == 1) or (isinstance(node.args[0], ast.Constant) and node.args[0].value == -1):
                self.uses_stack = True

        # Kadane pattern detection: max(..., current + ...)
        if func_name == "max" and len(node.args) >= 2:
            call_str = ast.unparse(node).lower() if hasattr(ast, "unparse") else ""
            if "+" in call_str and ("current" in call_str or "curr" in call_str or "sum" in call_str):
                self.has_kadane_pattern = True

        # Recursion detection (direct call to enclosing function or helper recursion)
        if self.function_stack and (func_name == self.function_stack[-1] or func_name in {"dfs", "helper", "backtrack", "search"}):
            self.recursive_call_count += 1
            self.has_recursion = True

        self.generic_visit(node)

    def get_features(self):
        detected_ds = []
        if self.uses_dictionary:
            detected_ds.append("Dictionary / Hash Map")
        if self.uses_set:
            detected_ds.append("Hash Set")
        if self.uses_heap:
            detected_ds.append("Min/Max Heap")
        if self.uses_deque:
            detected_ds.append("Double-Ended Queue (Deque)")
        if self.uses_stack:
            detected_ds.append("Stack (LIFO)")
        if self.uses_sorting:
            detected_ds.append("Sorting Routine")

        # Two-pointer determination
        has_paired_pointers = bool(
            {"left", "right"}.issubset(self.pointer_initializations)
            or {"l", "r"}.issubset(self.pointer_initializations)
            or {"low", "high"}.issubset(self.pointer_initializations)
            or {"start", "end"}.issubset(self.pointer_initializations)
            or {"i", "j"}.issubset(self.pointer_initializations)
            or {"slow", "fast"}.issubset(self.pointer_initializations)
        )
        has_two_pointers = (
            (has_paired_pointers and (self.has_converging_condition or self.has_pointer_adjustment))
            or (self.has_converging_condition and self.has_pointer_adjustment)
        )

        # Sliding window determination
        has_sliding_window = (
            not self.has_right_decrement and
            (
                (self.has_window_size_calc or self.has_window_contraction)
                or (has_paired_pointers and (self.uses_dictionary or self.uses_set) and self.has_pointer_adjustment)
            )
        )

        # Binary search determination
        has_binary_search = (
            self.has_mid_calc
            or (self.has_converging_condition and ("low" in self.pointer_initializations or "high" in self.pointer_initializations) and self.has_pointer_adjustment)
        )

        pointer_mechanics = []
        if has_paired_pointers:
            pointer_mechanics.append("Dual pointer initializations (e.g. left/right, start/end)")
        if self.has_converging_condition:
            pointer_mechanics.append("Converging loop boundary condition (e.g. left < right)")
        if self.has_pointer_adjustment:
            pointer_mechanics.append("Step-wise pointer updates (e.g. left += 1, right -= 1)")
        if self.has_window_contraction:
            pointer_mechanics.append("Window contraction logic (inner pointer advancement)")
        if self.has_window_size_calc:
            pointer_mechanics.append("Window span calculation (right - left + 1)")
        if self.has_mid_calc:
            pointer_mechanics.append("Binary midpoint computation ((left + right) // 2)")

        return {
            "function_count": self.function_count,
            "loop_count": self.loop_count,
            "max_loop_nesting": self.max_loop_nesting,
            "recursive_call_count": self.recursive_call_count,
            "has_recursion": self.has_recursion,
            "uses_dictionary": self.uses_dictionary,
            "uses_set": self.uses_set,
            "uses_sorting": self.uses_sorting,
            "uses_heap": self.uses_heap,
            "uses_deque": self.uses_deque,
            "uses_stack": self.uses_stack,
            "has_two_pointers": has_two_pointers,
            "has_sliding_window": has_sliding_window,
            "has_binary_search": has_binary_search,
            "has_monotonic_stack": self.has_stack_monotonic_pop,
            "has_kadane": self.has_kadane_pattern,
            "has_dp_table": self.has_dp_table,
            "detected_data_structures": detected_ds,
            "pointer_mechanics": pointer_mechanics,
        }