import re
from app.analyzer.pattern_matcher import (
    PATTERN_DISPLAY_NAMES,
    CANONICAL_APPROACH_NAMES,
    CANONICAL_PATTERN_EVIDENCE,
)
from app.analyzer.hint_generator import generate_hint
from app.knowledge_base import get_problem_by_id


def check_brackets_validity(code: str) -> tuple[bool, str | None, int | None]:
    """Check balanced braces, parentheses, and brackets for Java/C++ code."""
    # Strip block comments while preserving newlines
    clean = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), code, flags=re.DOTALL)
    stack = []
    lines = clean.splitlines()
    pairs = {')': '(', '}': '{', ']': '['}

    for line_idx, line in enumerate(lines, start=1):
        # Ignore single line comments
        line_clean = re.sub(r'//.*$', '', line)
        # Strip string literals and character literals
        line_clean = re.sub(r'"(\\.|[^"\\])*"', '""', line_clean)
        line_clean = re.sub(r"'(\\.|[^'\\])*'", "''", line_clean)

        for char in line_clean:
            if char in "({[":
                stack.append((char, line_idx))
            elif char in ")}]":
                if not stack:
                    return False, f"Unexpected closing '{char}'", line_idx
                top, top_line = stack.pop()
                if pairs[char] != top:
                    return False, f"Mismatched '{char}', expected closing for '{top}' from line {top_line}", line_idx

    if stack:
        top, top_line = stack.pop()
        return False, f"Unclosed '{top}' from line {top_line}", top_line

    return True, None, None


def analyze_c_style_code(code: str, language: str = "java", problem_id: int | None = None, hint_level: int = 1) -> dict:
    """
    Deterministic AST/structural static analysis for Java and C++ code.
    Identifies loops, recursion, data structures, pointer mechanics, and Big-O complexity.
    Produces identical pattern display name and evidence text as Python.
    """
    # 1. Syntax & bracket check
    is_valid, err_msg, err_line = check_brackets_validity(code)
    if not is_valid:
        return {
            "syntax_valid": False,
            "features": None,
            "pattern": None,
            "complexity": None,
            "hints": None,
            "hint": None,
            "problem_info": None,
            "error": {"line": err_line, "column": 1, "message": err_msg},
        }

    clean_code = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), code, flags=re.DOTALL)
    clean_code = re.sub(r'//.*$', '', clean_code, flags=re.MULTILINE)
    normalized = clean_code.casefold()

    # 2. Extract structural metrics using token-based brace tracking
    no_lit = re.sub(r'"(\\.|[^"\\])*"', '""', clean_code)
    no_lit = re.sub(r"'(\\.|[^'\\])*'", "''", no_lit)

    loop_count = 0
    max_loop_nesting = 0
    current_loop_nesting = 0
    brace_stack = []

    tokens = re.findall(r'\b(?:for|while)\b|[{}();]', no_lit)
    expect_loop_body = 0
    paren_depth = 0

    for tok in tokens:
        if tok in ('for', 'while'):
            loop_count += 1
            expect_loop_body += 1
        elif tok == '(':
            paren_depth += 1
        elif tok == ')':
            paren_depth = max(0, paren_depth - 1)
        elif tok == '{':
            if expect_loop_body > 0 and paren_depth == 0:
                is_loop = True
                expect_loop_body = max(0, expect_loop_body - 1)
                current_loop_nesting += 1
                max_loop_nesting = max(max_loop_nesting, current_loop_nesting)
            else:
                is_loop = False
            brace_stack.append(is_loop)
        elif tok == '}':
            if brace_stack:
                was_loop = brace_stack.pop()
                if was_loop:
                    current_loop_nesting = max(0, current_loop_nesting - 1)

    # Data structures detection
    uses_dictionary = False
    uses_set = False
    uses_heap = False
    uses_deque = False
    uses_stack = False
    uses_sorting = False

    detected_ds = []

    if language.lower() == "java":
        if re.search(r'\b(hashmap|map<|treemap)\b', normalized) or " - 'a'" in normalized or "-'a'" in normalized:
            uses_dictionary = True
            detected_ds.append("HashMap (Key-Value)")
        if re.search(r'\b(hashset|set<|treeset)\b', normalized):
            uses_set = True
            detected_ds.append("HashSet (O(1) Set)")
        if "priorityqueue" in normalized:
            uses_heap = True
            detected_ds.append("PriorityQueue (Heap)")
        if ("arraydeque" in normalized or "deque" in normalized or "queue" in normalized) and not ("push(" in normalized or ".push(" in normalized):
            uses_deque = True
            detected_ds.append("Deque (Queue)")
        if "stack" in normalized or ".push(" in normalized or "push(" in normalized:
            uses_stack = True
            detected_ds.append("Stack (LIFO)")
        if "arrays.sort" in normalized or "collections.sort" in normalized:
            uses_sorting = True
            detected_ds.append("Sorting Routine")
    else:  # C++
        if re.search(r'\b(unordered_map|map)\b', normalized) or " - 'a'" in normalized or "-'a'" in normalized:
            uses_dictionary = True
            detected_ds.append("unordered_map (Hash Table)")
        if re.search(r'\b(unordered_set|set)\b', normalized):
            uses_set = True
            detected_ds.append("unordered_set (Hash Set)")
        if "priority_queue" in normalized:
            uses_heap = True
            detected_ds.append("priority_queue (Heap)")
        if "queue" in normalized and not ("push_back" in normalized or "pop_back" in normalized):
            uses_deque = True
            detected_ds.append("queue / deque")
        if "stack" in normalized or "pop_back" in normalized or ".back()" in normalized:
            uses_stack = True
            detected_ds.append("stack (LIFO)")
        if "std::sort" in normalized or "sort(" in normalized:
            uses_sorting = True
            detected_ds.append("std::sort (Introsort)")

    # Two-pointer signals
    has_paired_pointers = bool(
        re.search(r'\b(left|l|low|start|p1)\b', normalized) and re.search(r'\b(right|r|high|end|p2)\b', normalized)
    )
    has_converging_cond = bool(
        re.search(r'while\s*\(\s*(left|l|low|start|i)\s*<=\s*(right|r|high|end|j)\s*\)', normalized) or
        re.search(r'while\s*\(\s*(left|l|low|start|i)\s*<\s*(right|r|high|end|j)\s*\)', normalized)
    )
    has_pointer_adjust = bool(
        re.search(r'\b(left|l|start|low)\s*(\+\+|\+=|=)', normalized) and
        re.search(r'\b(right|r|end|high)\s*(--|-=|=)', normalized)
    )
    has_right_decrement = bool(re.search(r'\b(right|r|end|high)\s*(--|-=)', normalized))
    has_two_pointers = (has_paired_pointers and (has_converging_cond or has_pointer_adjust)) or (has_converging_cond and has_pointer_adjust)

    # Sliding window signals
    has_window_span = bool(
        "right - left + 1" in normalized or "r - l + 1" in normalized or "end - start + 1" in normalized or
        "right-left+1" in normalized or "r-l+1" in normalized
    )
    has_sliding_window = (not has_right_decrement) and (has_window_span or (has_paired_pointers and (uses_dictionary or uses_set) and has_pointer_adjust))

    # Binary search signals (includes low + (high - low) / 2 and standard variants)
    has_mid_calc = bool(
        (re.search(r'\b(mid|m)\s*=', normalized) and ("/2" in normalized or "/ 2" in normalized or ">>1" in normalized or ">> 1" in normalized)) or
        bool(re.search(r'\(\s*(?:r|right|high)\s*-\s*(?:l|left|low)\s*\)\s*/\s*2', normalized)) or
        bool(re.search(r'\(\s*(?:l|left|low)\s*\+\s*(?:r|right|high)\s*\)\s*/\s*2', normalized)) or
        bool(re.search(r'\(\s*(?:l|left|low)\s*\+\s*(?:r|right|high)\s*\)\s*>>\s*1', normalized))
    )
    has_binary_search = has_mid_calc or (has_converging_cond and ("low" in normalized or "high" in normalized) and ("mid" in normalized or ">>" in normalized))

    # Kadane signals
    has_kadane = bool(
        ("max" in normalized) and
        ("current" in normalized or "curr" in normalized or "cur" in normalized or "max_so_far" in normalized) and
        ("+" in normalized or "sum" in normalized) and
        not ("min" in normalized or "minprice" in normalized or "mn" in normalized) and
        max_loop_nesting <= 1 and loop_count >= 1
    )

    # Prefix sum / product signals
    has_prefix_sum = bool(
        ("prefix" in normalized or "suffix" in normalized) and
        max_loop_nesting <= 1 and loop_count >= 1
    )

    # Monotonic stack signals
    has_monotonic_stack = bool(
        uses_stack and (".pop(" in normalized or "pop(" in normalized or "pop_back" in normalized) and ("while" in normalized)
    )

    # Recursion / DFS signals: method calls itself (occurs >= 2 times) or calls recursive helper
    has_recursion = False
    if re.search(r'\b(dfs|helper|traverse|backtrack)\s*\(', normalized):
        has_recursion = True
    else:
        method_defs = re.findall(r'(?:public\s+|private\s+|protected\s+)?(?:[\w<>\[\]]+)\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*\{', clean_code)
        for m_name in method_defs:
            m_lower = m_name.lower()
            if m_lower in {"solution", "treenode", "listnode", "node", "minstack", "worddictionary", "main"}:
                continue
            calls = len(re.findall(r'\b' + re.escape(m_name) + r'\s*\(', clean_code, flags=re.IGNORECASE))
            if calls >= 2:
                has_recursion = True
                break

    # Dynamic programming signals
    has_dp_table = bool(
        re.search(r'\b(dp\[|memo\[|table\[|new int\[amount|new int\[n \+|int\[\] dp|vector<int> dp|vector<vector<int>> dp)', normalized)
    )

    pointer_mechanics = []
    if has_paired_pointers:
        pointer_mechanics.append("Two index pointers declared (left & right)")
    if has_converging_cond:
        pointer_mechanics.append("Loop bounds test: while (left < right)")
    if has_pointer_adjust:
        pointer_mechanics.append("Pointers moving inward: left++ / right--")
    if has_window_span:
        pointer_mechanics.append("Window length calculation: right - left + 1")
    if has_mid_calc:
        pointer_mechanics.append("Midpoint division: mid = (low + high) / 2")

    features = {
        "loop_count": loop_count,
        "max_loop_nesting": max_loop_nesting,
        "uses_dictionary": uses_dictionary,
        "uses_set": uses_set,
        "uses_sorting": uses_sorting,
        "uses_heap": uses_heap,
        "uses_deque": uses_deque,
        "uses_stack": uses_stack,
        "has_two_pointers": has_two_pointers,
        "has_sliding_window": has_sliding_window,
        "has_binary_search": has_binary_search,
        "has_monotonic_stack": has_monotonic_stack,
        "has_kadane": has_kadane,
        "has_recursion": has_recursion,
        "has_dp_table": has_dp_table,
        "detected_data_structures": detected_ds,
        "pointer_mechanics": pointer_mechanics,
    }

    # 3. Match Pattern (consistent priority matching Python pattern_matcher)
    problem = get_problem_by_id(problem_id) if problem_id else None
    optimal_approach_name = problem["primary_solution"]["approach"] if problem and "primary_solution" in problem else None

    pattern_name = "unknown"
    confidence = "low"
    is_optimal = False
    alt = optimal_approach_name

    # Priority matching order synchronized with Python
    if has_monotonic_stack:
        pattern_name = "monotonic_stack"
        confidence = "high"
        is_optimal = True
    elif has_binary_search:
        pattern_name = "binary_search"
        confidence = "high"
        is_optimal = True
    elif uses_sorting and (has_two_pointers or has_converging_cond):
        pattern_name = "sorting_two_pointers"
        confidence = "high"
        is_optimal = True
    elif has_sliding_window:
        pattern_name = "sliding_window"
        confidence = "high"
        is_optimal = True
    elif has_two_pointers:
        pattern_name = "two_pointers"
        confidence = "high"
        is_optimal = True
    elif has_kadane:
        pattern_name = "kadane"
        confidence = "high"
        is_optimal = True
    elif has_prefix_sum:
        pattern_name = "prefix_sum"
        confidence = "high"
        is_optimal = True
    elif uses_set and ("contains" in normalized or "count" in normalized or ".find" in normalized or "insert" in normalized):
        pattern_name = "hash_set"
        confidence = "high"
        is_optimal = True
    elif uses_dictionary:
        pattern_name = "hash_map"
        confidence = "high"
        is_optimal = True
    elif uses_heap:
        pattern_name = "heap"
        confidence = "high"
        is_optimal = True
    elif uses_deque and ("poll" in normalized or "pop" in normalized or "front" in normalized):
        pattern_name = "bfs"
        confidence = "high"
        is_optimal = True
    elif has_recursion:
        pattern_name = "dfs"
        confidence = "medium"
        is_optimal = True
    elif has_dp_table:
        pattern_name = "dynamic_programming"
        confidence = "medium"
        is_optimal = True
    elif max_loop_nesting >= 2 and loop_count >= 2:
        pattern_name = "brute_force"
        confidence = "high"
        is_optimal = False
        alt = optimal_approach_name or "hash_map"
    elif max_loop_nesting == 1 and loop_count >= 1 and ("min" in normalized or "max" in normalized or "best" in normalized):
        pattern_name = "greedy"
        confidence = "medium"
        is_optimal = True

    # Pull canonical synchronized evidence
    evidence = list(CANONICAL_PATTERN_EVIDENCE.get(pattern_name, CANONICAL_PATTERN_EVIDENCE["unknown"]))
    if pattern_name == "hash_map":
        if "complement" in normalized or "target -" in normalized or "target-" in normalized:
            evidence.append("A possible complement calculation was detected.")

    pattern_result = {
        "name": pattern_name,
        "display_name": PATTERN_DISPLAY_NAMES.get(pattern_name, "In-Progress / Drafting Solution"),
        "confidence": confidence,
        "evidence": evidence,
        "alternative": alt if not is_optimal else None,
        "is_optimal": is_optimal,
        "matched_approach_name": CANONICAL_APPROACH_NAMES.get(pattern_name, pattern_name.replace("_", " ").title()),
    }

    # 4. Complexity estimation
    target_complexity = problem["primary_solution"]["complexity"] if problem and "primary_solution" in problem else {"time": "O(n)", "space": "O(1)"}
    
    comp_time = "O(1)"
    comp_space = "O(1)"
    comp_evidence = []

    if uses_dictionary or uses_set or uses_stack:
        comp_space = "O(n)"
        comp_evidence.append(f"Uses auxiliary {language.capitalize()} collection (up to O(n) space).")
    else:
        comp_space = "O(1)"
        comp_evidence.append("Only scalar pointer variables used (O(1) minimal space).")

    if has_binary_search:
        comp_time = "O(log n)"
        comp_evidence.append("Binary search logarithmic time.")
    elif uses_sorting:
        comp_time = "O(n log n)"
        comp_evidence.append("Standard comparison sort takes O(n log n) time.")
    elif has_sliding_window or has_two_pointers or max_loop_nesting == 1:
        comp_time = "O(n)"
        comp_evidence.append("Single linear traversal takes O(n) time.")
    elif max_loop_nesting >= 2:
        comp_time = f"O(n^{max_loop_nesting})"
        comp_evidence.append(f"{max_loop_nesting} nested loops take O(n^{max_loop_nesting}) polynomial time.")

    efficiency = "Optimal Speed" if comp_time == target_complexity.get("time") else "Suboptimal (Slow Quadratic O(n²))" if "n^2" in comp_time else "Can Be Faster"

    complexity_result = {
        "status": "estimated",
        "time": comp_time,
        "space": comp_space,
        "evidence": comp_evidence,
        "target_time": target_complexity.get("time", "O(n)"),
        "target_space": target_complexity.get("space", "O(1)"),
        "efficiency_rating": efficiency,
    }

    hints = {
        1: generate_hint(problem_id, pattern_name, 1),
        2: generate_hint(problem_id, pattern_name, 2),
        3: generate_hint(problem_id, pattern_name, 3),
    }

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
        "hint": hints.get(hint_level, hints[1]),
        "problem_info": problem_info,
        "error": None,
    }
