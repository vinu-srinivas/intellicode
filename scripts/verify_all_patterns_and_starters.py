import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.knowledge_base import load_problems, public_problem_details
from app.analyzer.analyzer import analyze_code

def verify_all():
    problems = load_problems()
    print(f"Loaded {len(problems)} problems.")

    starter_pattern_mismatches = []
    starter_syntax_errors = []
    optimal_syntax_errors = []
    optimal_pattern_mismatches = []
    metadata_issues = []

    for p in problems:
        pid = p["leetcode_id"]
        pub = public_problem_details(p)

        # 1. Metadata checks
        desc = pub.get("description", "")
        if not desc or len(desc) < 20:
            metadata_issues.append((pid, "description too short or missing"))

        examples = pub.get("examples", [])
        if len(examples) < 2:
            metadata_issues.append((pid, f"fewer than 2 examples ({len(examples)})"))

        constraints = pub.get("constraints", [])
        if len(constraints) < 2:
            metadata_issues.append((pid, f"fewer than 2 constraints ({len(constraints)})"))

        test_cases = pub.get("test_cases", [])
        if len(test_cases) < 2:
            metadata_issues.append((pid, f"fewer than 2 test cases ({len(test_cases)})"))

        starters = pub.get("starter_codes", {})
        for lang in ["python", "java", "cpp"]:
            if not starters.get(lang):
                metadata_issues.append((pid, f"missing starter code for {lang}"))

        # 2. Starter code pattern consistency checks
        py_start = starters.get("python", "")
        ja_start = starters.get("java", "")
        cp_start = starters.get("cpp", "")

        py_res = analyze_code(code=py_start, problem_id=pid, language="python")
        ja_res = analyze_code(code=ja_start, problem_id=pid, language="java")
        cp_res = analyze_code(code=cp_start, problem_id=pid, language="cpp")

        if not py_res.get("syntax_valid"):
            starter_syntax_errors.append((pid, "python", py_res.get("error")))
        if not ja_res.get("syntax_valid"):
            starter_syntax_errors.append((pid, "java", ja_res.get("error")))
        if not cp_res.get("syntax_valid"):
            starter_syntax_errors.append((pid, "cpp", cp_res.get("error")))

        py_pat = py_res.get("pattern") or {}
        ja_pat = ja_res.get("pattern") or {}
        cp_pat = cp_res.get("pattern") or {}

        # Check starter pattern alignment
        if py_pat.get("display_name") != ja_pat.get("display_name") or py_pat.get("display_name") != cp_pat.get("display_name"):
            starter_pattern_mismatches.append((pid, "display_name", py_pat.get("display_name"), ja_pat.get("display_name"), cp_pat.get("display_name")))
        if py_pat.get("evidence") != ja_pat.get("evidence") or py_pat.get("evidence") != cp_pat.get("evidence"):
            starter_pattern_mismatches.append((pid, "evidence", py_pat.get("evidence"), ja_pat.get("evidence"), cp_pat.get("evidence")))

        # 3. Primary solution pattern consistency checks
        sol_code = p.get("primary_solution", {}).get("code", {})
        if isinstance(sol_code, dict):
            py_opt = sol_code.get("python", "")
            ja_opt = sol_code.get("java", "")
            cp_opt = sol_code.get("cpp", "")

            py_opt_res = analyze_code(code=py_opt, problem_id=pid, language="python")
            ja_opt_res = analyze_code(code=ja_opt, problem_id=pid, language="java")
            cp_opt_res = analyze_code(code=cp_opt, problem_id=pid, language="cpp")

            if not py_opt_res.get("syntax_valid"):
                optimal_syntax_errors.append((pid, "python", py_opt_res.get("error")))
            if not ja_opt_res.get("syntax_valid"):
                optimal_syntax_errors.append((pid, "java", ja_opt_res.get("error")))
            if not cp_opt_res.get("syntax_valid"):
                optimal_syntax_errors.append((pid, "cpp", cp_opt_res.get("error")))

            py_opt_pat = py_opt_res.get("pattern") or {}
            ja_opt_pat = ja_opt_res.get("pattern") or {}
            cp_opt_pat = cp_opt_res.get("pattern") or {}

            if py_opt_pat.get("display_name") != ja_opt_pat.get("display_name") or py_opt_pat.get("display_name") != cp_opt_pat.get("display_name"):
                optimal_pattern_mismatches.append((
                    pid,
                    p["title"],
                    f"PY: {py_opt_pat.get('display_name')}",
                    f"JA: {ja_opt_pat.get('display_name')}",
                    f"CP: {cp_opt_pat.get('display_name')}"
                ))

    print(f"\nMetadata issues: {len(metadata_issues)}")
    for issue in metadata_issues:
        print(" ", issue)

    print(f"\nStarter syntax errors: {len(starter_syntax_errors)}")
    for err in starter_syntax_errors:
        print(" ", err)

    print(f"\nStarter pattern mismatches: {len(starter_pattern_mismatches)}")
    for mm in starter_pattern_mismatches:
        print(" ", mm)

    print(f"\nOptimal syntax errors: {len(optimal_syntax_errors)}")
    for err in optimal_syntax_errors:
        print(" ", err)

    print(f"\nOptimal pattern mismatches: {len(optimal_pattern_mismatches)}")
    for mm in optimal_pattern_mismatches[:20]:
        print(" ", mm)
    if len(optimal_pattern_mismatches) > 20:
        print(f" ... and {len(optimal_pattern_mismatches) - 20} more")

if __name__ == "__main__":
    verify_all()
