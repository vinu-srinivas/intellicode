import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.runner import run_code_tests
from app.knowledge_base import get_problem_by_id, public_problem_details

def test_runner():
    p1 = get_problem_by_id(1)
    p70 = get_problem_by_id(70)
    p70_pub = public_problem_details(p70)

    print("--- Testing Problem 1 (Two Sum) ---")
    py_code = p1["primary_solution"]["code"]["python"]
    res_py = run_code_tests(py_code, 1, "python")
    print("Py optimal:", res_py["success"], f"{res_py['passed']}/{res_py['total']}", res_py.get("error"))

    java_code = p1["primary_solution"]["code"]["java"]
    res_java = run_code_tests(java_code, 1, "java")
    print("Java optimal:", res_java["success"], f"{res_java['passed']}/{res_java['total']}", res_java.get("error"))

    cpp_code = p1["primary_solution"]["code"]["cpp"]
    res_cpp = run_code_tests(cpp_code, 1, "cpp")
    print("C++ optimal:", res_cpp["success"], f"{res_cpp['passed']}/{res_cpp['total']}", res_cpp.get("error"))

    print("\n--- Testing Problem 70 (Climbing Stairs - Fallback harness) ---")
    java_starter = p70_pub["starter_codes"]["java"]
    res_java_start = run_code_tests(java_starter, 70, "java")
    print("Java starter:", res_java_start["success"], f"{res_java_start['passed']}/{res_java_start['total']}", res_java_start.get("error"))

    cpp_starter = p70_pub["starter_codes"]["cpp"]
    res_cpp_start = run_code_tests(cpp_starter, 70, "cpp")
    print("C++ starter:", res_cpp_start["success"], f"{res_cpp_start['passed']}/{res_cpp_start['total']}", res_cpp_start.get("error"))

    print("\n--- Testing Problem 70 Optimal ---")
    py70 = p70["primary_solution"]["code"]["python"]
    res_py70 = run_code_tests(py70, 70, "python")
    print("Py 70 optimal:", res_py70["success"], f"{res_py70['passed']}/{res_py70['total']}", res_py70.get("error"))

    java70 = p70["primary_solution"]["code"]["java"]
    res_java70 = run_code_tests(java70, 70, "java")
    print("Java 70 optimal:", res_java70["success"], f"{res_java70['passed']}/{res_java70['total']}", res_java70.get("error"))

    cpp70 = p70["primary_solution"]["code"]["cpp"]
    res_cpp70 = run_code_tests(cpp70, 70, "cpp")
    print("C++ 70 optimal:", res_cpp70["success"], f"{res_cpp70['passed']}/{res_cpp70['total']}", res_cpp70.get("error"))

if __name__ == "__main__":
    test_runner()
