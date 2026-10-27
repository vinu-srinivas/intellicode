import json
from functools import lru_cache
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "codebase.json"


from app.curated_problems_data import CURATED_PROBLEM_EXTRAS



def extract_starter_code(code_str: str, language: str = "python") -> str:
    """Extract class and method signatures to provide a clean skeleton starter template."""
    if not code_str:
        if language == "java":
            return "class Solution {\n    public int[] solve() {\n        // Write your solution here\n        return new int[0];\n    }\n}\n"
        elif language in {"cpp", "c++"}:
            return "class Solution {\npublic:\n    void solve() {\n        // Write your solution here\n    }\n};\n"
        return "class Solution:\n    def solve(self):\n        # Write your solution here\n        pass\n"

    lines = code_str.strip().splitlines()

    if language == "python":
        header_lines = []
        found_def = False
        for line in lines:
            s = line.strip()
            if s.startswith("class "):
                colon = line.find(":")
                header_lines.append(line[:colon + 1] if colon != -1 else line)
            elif s.startswith("def "):
                paren_close = line.rfind(")")
                if paren_close != -1:
                    colon = line.find(":", paren_close)
                    def_line = line[:colon + 1] if colon != -1 else line
                else:
                    colon = line.rfind(":")
                    def_line = line[:colon + 1] if colon != -1 else line
                header_lines.append("    " + def_line.strip())
                found_def = True
                break
        if not found_def or not header_lines:
            return "class Solution:\n    def solve(self):\n        # Write your solution here\n        pass\n"

        header_lines.append("        # Write your solution here\n        pass")
        return "\n".join(header_lines) + "\n"

    elif language == "java":
        sig_line = ""
        imports = []
        candidates = []
        for line in lines:
            s = line.strip()
            if s.startswith("import "):
                imports.append(s)
            elif "public " in s and "(" in s and "class " not in s:
                idx = s.find("{")
                candidate = s[:idx].strip() if idx != -1 else s
                candidates.append(candidate)

        for cand in candidates:
            cand_name = cand[:cand.find("(")].strip().split()[-1]
            if cand_name not in ["dfs", "bfs", "helper", "expand", "backtrack"]:
                sig_line = cand
                break
        if not sig_line and candidates:
            sig_line = candidates[0]

        if not sig_line:
            return "class Solution {\n    public int[] solve() {\n        // Write your solution here\n        return new int[0];\n    }\n}\n"

        before_paren = sig_line[:sig_line.find("(")].strip()
        parts = before_paren.split()
        ret_type = parts[-2] if len(parts) >= 2 else ""

        ret = "return null;"
        if "boolean[][]" in ret_type:
            ret = "return new boolean[0][0];"
        elif "boolean[]" in ret_type:
            ret = "return new boolean[0];"
        elif "boolean" in ret_type:
            ret = "return false;"
        elif "int[][]" in ret_type:
            ret = "return new int[0][0];"
        elif "int[]" in ret_type:
            ret = "return new int[0];"
        elif "char[][]" in ret_type:
            ret = "return new char[0][0];"
        elif any(t in ret_type for t in ["int", "long", "double", "float"]):
            ret = "return 0;"
        elif "List" in ret_type:
            ret = "return new ArrayList<>();"
        elif "String" in ret_type:
            ret = "return \"\";"
        elif "void" in ret_type:
            ret = ""

        res = []
        if imports:
            res.extend(imports)
        res.append("class Solution {")
        res.append(f"    {sig_line} {{")
        res.append("        // Write your solution here")
        if ret:
            res.append(f"        {ret}")
        res.append("    }")
        res.append("}\n")
        return "\n".join(res)

    else:  # C++
        sig_line = ""
        includes = []
        in_public = False
        candidates = []
        for line in lines:
            s = line.strip()
            if s.startswith("#include") or s.startswith("using "):
                includes.append(s)
            elif "public:" in s:
                in_public = True
            elif "(" in s and "class " not in s and "public:" not in s and "private:" not in s:
                idx = s.find("{")
                candidate = s[:idx].strip() if idx != -1 else s
                candidates.append((candidate, in_public))

        for cand, is_pub in candidates:
            cand_name = cand[:cand.find("(")].strip().split()[-1].lstrip("*&")
            if is_pub and cand_name not in ["dfs", "bfs", "helper", "back", "h", "ok", "gain", "build"]:
                sig_line = cand
                break
        if not sig_line:
            for cand, _ in candidates:
                cand_name = cand[:cand.find("(")].strip().split()[-1].lstrip("*&")
                if cand_name not in ["dfs", "bfs", "helper", "back", "h", "ok", "gain", "build"]:
                    sig_line = cand
                    break
        if not sig_line and candidates:
            sig_line = candidates[-1][0] if len(candidates) > 1 else candidates[0][0]

        if not sig_line:
            return "class Solution {\npublic:\n    void solve() {\n        // Write your solution here\n    }\n};\n"

        before_paren = sig_line[:sig_line.find("(")].strip()
        parts = before_paren.split()
        ret_type = parts[-2] if len(parts) >= 2 else ""

        ret = "return {};"
        if "vector" in ret_type or "string" in ret_type:
            ret = "return {};"
        elif "bool" in ret_type:
            ret = "return false;"
        elif any(t in ret_type for t in ["int", "long", "double", "float"]):
            ret = "return 0;"
        elif "void" in ret_type:
            ret = ""
        elif "*" in ret_type or "*" in sig_line[:sig_line.find("(")]:
            ret = "return nullptr;"

        res = []
        if includes:
            res.extend(includes)
            res.append("")
        res.append("class Solution {")
        res.append("public:")
        res.append(f"    {sig_line} {{")
        res.append("        // Write your solution here")
        if ret:
            res.append(f"        {ret}")
        res.append("    }")
        res.append("};\n")
        return "\n".join(res)



@lru_cache(maxsize=1)
def load_problems():
    """Load and validate the DSA problem knowledge base."""
    if not KNOWLEDGE_BASE_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_BASE_PATH}"
        )

    try:
        with KNOWLEDGE_BASE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {KNOWLEDGE_BASE_PATH}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError("Knowledge base must contain a JSON object.")

    problems = data.get("problems")
    if not isinstance(problems, list):
        raise ValueError("Knowledge base must contain a 'problems' list.")

    seen_ids = set()
    for problem in problems:
        if not isinstance(problem, dict):
            raise ValueError("Every problem must be a JSON object.")

        required_fields = [
            "rank",
            "leetcode_id",
            "title",
            "difficulty",
            "category",
            "patterns",
            "approaches",
            "primary_solution",
        ]

        for field in required_fields:
            if field not in problem:
                raise ValueError(
                    f"Problem is missing required field: {field}"
                )

        problem_id = problem["leetcode_id"]
        if (
            isinstance(problem_id, bool)
            or not isinstance(problem_id, int)
            or problem_id <= 0
        ):
            raise ValueError(f"Invalid LeetCode ID: {problem_id}")

        if problem_id in seen_ids:
            raise ValueError(f"Duplicate LeetCode ID: {problem_id}")

        seen_ids.add(problem_id)

    return problems


def get_problem_by_id(leetcode_id: int):
    """Find a problem using its LeetCode ID."""
    for problem in load_problems():
        if problem["leetcode_id"] == leetcode_id:
            return problem
    return None


def public_problem_summary(problem: dict):
    """Return problem metadata without reference solutions."""
    return {
        "rank": problem["rank"],
        "leetcode_id": problem["leetcode_id"],
        "title": problem["title"],
        "difficulty": problem["difficulty"],
        "category": problem["category"],
        "patterns": problem["patterns"],
    }


def public_problem_details(problem: dict):
    """Return problem details including multi-language approaches, starter codes, and descriptions."""
    approaches = []
    for approach in problem["approaches"]:
        approaches.append(
            {
                "name": approach["name"],
                "idea": approach["idea"],
                "complexity": approach["complexity"],
                "code": approach.get("code", {}),
            }
        )

    problem_id = problem["leetcode_id"]
    extras = CURATED_PROBLEM_EXTRAS.get(problem_id, {})

    py_solution = problem.get("primary_solution", {}).get("code", {}).get("python", "")
    java_solution = problem.get("primary_solution", {}).get("code", {}).get("java", "")
    cpp_solution = problem.get("primary_solution", {}).get("code", {}).get("cpp", "")

    curated_starters = extras.get("starter_codes")
    if curated_starters:
        starter_codes = curated_starters
    else:
        starter_codes = {
            "python": extract_starter_code(py_solution, "python"),
            "java": extract_starter_code(java_solution, "java"),
            "cpp": extract_starter_code(cpp_solution, "cpp"),
        }

    description = extras.get(
        "description",
        f"Solve the classic '{problem['title']}' problem ({problem['category']}). Implement an optimal algorithm using the '{problem['primary_solution']['approach']}' pattern."
    )
    examples = extras.get("examples", [])
    constraints = extras.get(
        "constraints",
        ["Optimize for time and space complexity according to the problem requirements."]
    )
    test_cases = extras.get("test_cases", [])

    return {
        **public_problem_summary(problem),
        "approaches": approaches,
        "primary_approach": problem["primary_solution"]["approach"],
        "primary_complexity": problem["primary_solution"]["complexity"],
        "primary_code": problem.get("primary_solution", {}).get("code", {}),
        "starter_code": starter_codes["python"],
        "starter_codes": starter_codes,
        "description": description,
        "examples": examples,
        "constraints": constraints,
        "test_cases": test_cases,
    }