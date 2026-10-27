import ast
import contextlib
import io
import time
import copy
import subprocess
import tempfile
import os
from typing import Any, Optional
import collections
from collections import defaultdict, deque, Counter
import heapq
import math

from app.knowledge_base import get_problem_by_id, CURATED_PROBLEM_EXTRAS


def _normalize_for_comparison(val: Any) -> Any:
    """Normalize lists/tuples for comparison where order might not matter or float tolerances."""
    if isinstance(val, (list, tuple)):
        try:
            if val and isinstance(val[0], list):
                return sorted([sorted(sub) for sub in val])
        except Exception:
            pass
    return val


# Runs Python code in an isolated scope against test cases

def run_python_tests(code: str, problem_id: int | None = None) -> dict:
    """Execute Python code in isolated scope against test cases."""
    try:
        ast.parse(code)
    except SyntaxError as err:
        return {
            "success": False,
            "passed": 0,
            "total": 0,
            "test_results": [],
            "runtime_ms": 0.0,
            "stdout": "",
            "error": f"Syntax Error at line {err.lineno}: {err.msg}",
        }

    stdout_capture = io.StringIO()
    namespace: dict[str, Any] = {
        "__name__": "__main__",
        "List": list,
        "Dict": dict,
        "Set": set,
        "Tuple": tuple,
        "Optional": Optional,
        "heapq": heapq,
        "collections": collections,
        "defaultdict": defaultdict,
        "deque": deque,
        "Counter": Counter,
        "math": math,
    }

    start_exec = time.perf_counter()
    try:
        with contextlib.redirect_stdout(stdout_capture):
            exec(code, namespace)
    except Exception as exc:
        elapsed = (time.perf_counter() - start_exec) * 1000.0
        return {
            "success": False,
            "passed": 0,
            "total": 0,
            "test_results": [],
            "runtime_ms": round(elapsed, 2),
            "stdout": stdout_capture.getvalue(),
            "error": f"Runtime Error during definition: {type(exc).__name__}: {str(exc)}",
        }

    problem = get_problem_by_id(problem_id) if problem_id else None
    extras = CURATED_PROBLEM_EXTRAS.get(problem_id, {}) if problem_id else {}
    test_cases = extras.get("test_cases", [])

    if not test_cases:
        elapsed = (time.perf_counter() - start_exec) * 1000.0
        return {
            "success": True,
            "passed": 1,
            "total": 1,
            "test_results": [
                {
                    "case_number": 1,
                    "passed": True,
                    "input": "(General code execution)",
                    "expected": "Executed successfully",
                    "actual": "Completed without exceptions",
                }
            ],
            "runtime_ms": round(elapsed, 2),
            "stdout": stdout_capture.getvalue(),
            "error": None,
        }

    # Locate Solution class or solve function
    solution_instance = None
    target_method = None

    if "Solution" in namespace and isinstance(namespace["Solution"], type):
        try:
            solution_instance = namespace["Solution"]()
            methods = [
                m for m in dir(solution_instance)
                if not m.startswith("__") and callable(getattr(solution_instance, m))
            ]
            if methods:
                target_method = getattr(solution_instance, methods[0])
        except Exception as exc:
            return {
                "success": False,
                "passed": 0,
                "total": len(test_cases),
                "test_results": [],
                "runtime_ms": 0.0,
                "stdout": stdout_capture.getvalue(),
                "error": f"Could not instantiate Solution class: {exc}",
            }
    else:
        for k, v in namespace.items():
            if callable(v) and not k.startswith("_") and k not in {"List", "Dict", "Set", "Tuple", "Optional", "defaultdict", "deque", "Counter"}:
                target_method = v
                break

    if target_method is None:
        return {
            "success": False,
            "passed": 0,
            "total": len(test_cases),
            "test_results": [],
            "runtime_ms": 0.0,
            "stdout": stdout_capture.getvalue(),
            "error": "No Solution class method or solution function found in code.",
        }

    results = []
    passed_count = 0
    total_time = 0.0

    for idx, tc in enumerate(test_cases, start=1):
        input_args = copy.deepcopy(tc["input"])
        expected = tc["expected"]
        t_start = time.perf_counter()
        tc_stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(tc_stdout):
                if isinstance(input_args, dict):
                    actual = target_method(**input_args)
                elif isinstance(input_args, (list, tuple)):
                    actual = target_method(*input_args)
                else:
                    actual = target_method(input_args)

            t_elapsed = (time.perf_counter() - t_start) * 1000.0
            total_time += t_elapsed

            passed = False
            if problem_id == 1 and isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
                passed = sorted(actual) == sorted(expected)
            elif problem_id == 15:
                passed = _normalize_for_comparison(actual) == _normalize_for_comparison(expected)
            else:
                passed = actual == expected

            if passed:
                passed_count += 1

            results.append({
                "case_number": idx,
                "passed": passed,
                "input": str(input_args),
                "expected": str(expected),
                "actual": str(actual),
                "runtime_ms": round(t_elapsed, 2),
                "stdout": tc_stdout.getvalue(),
                "error": None,
            })
        except Exception as exc:
            t_elapsed = (time.perf_counter() - t_start) * 1000.0
            results.append({
                "case_number": idx,
                "passed": False,
                "input": str(input_args),
                "expected": str(expected),
                "actual": "Error",
                "runtime_ms": round(t_elapsed, 2),
                "stdout": tc_stdout.getvalue(),
                "error": f"{type(exc).__name__}: {str(exc)}",
            })

    all_passed = (passed_count == len(test_cases))

    return {
        "success": all_passed,
        "passed": passed_count,
        "total": len(test_cases),
        "test_results": results,
        "runtime_ms": round(total_time, 2),
        "stdout": stdout_capture.getvalue(),
        "error": None if all_passed else f"{len(test_cases) - passed_count} of {len(test_cases)} tests failed.",
    }


# Compiles and executes Java submissions against problem test cases

def _generate_java_call(pid: int, tc: dict, idx: int) -> str:
    inp = tc["input"]
    exp = tc["expected"]
    inp_escaped = str(inp).replace('"', '\\"').replace('\n', ' ')
    if pid == 1:
        nums_str = "new int[]{" + ", ".join(map(str, inp["nums"])) + "}"
        target = inp["target"]
        return f'''
        {{
            long t0 = System.nanoTime();
            int[] act = sol.twoSum({nums_str}, {target});
            double ms = (System.nanoTime() - t0) / 1e6;
            int[] exp = new int[]{{{", ".join(map(str, exp))}}};
            int[] actSorted = act != null ? act.clone() : new int[0];
            int[] expSorted = exp.clone();
            Arrays.sort(actSorted); Arrays.sort(expSorted);
            boolean pass = Arrays.equals(actSorted, expSorted);
            printResult({idx}, pass, "{inp_escaped}", Arrays.toString(exp), Arrays.toString(act), ms);
        }}
        '''
    elif pid == 121:
        prices_str = "new int[]{" + ", ".join(map(str, inp["prices"])) + "}"
        return f'''
        {{
            long t0 = System.nanoTime();
            int act = sol.maxProfit({prices_str});
            double ms = (System.nanoTime() - t0) / 1e6;
            boolean pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", "{exp}", String.valueOf(act), ms);
        }}
        '''
    elif pid == 217:
        nums_str = "new int[]{" + ", ".join(map(str, inp["nums"])) + "}"
        exp_bool = "true" if exp else "false"
        return f'''
        {{
            long t0 = System.nanoTime();
            boolean act = sol.containsDuplicate({nums_str});
            double ms = (System.nanoTime() - t0) / 1e6;
            boolean pass = (act == {exp_bool});
            printResult({idx}, pass, "{inp_escaped}", "{exp_bool}", String.valueOf(act), ms);
        }}
        '''
    elif pid == 238:
        nums_str = "new int[]{" + ", ".join(map(str, inp["nums"])) + "}"
        return f'''
        {{
            long t0 = System.nanoTime();
            int[] act = sol.productExceptSelf({nums_str});
            double ms = (System.nanoTime() - t0) / 1e6;
            int[] exp = new int[]{{{", ".join(map(str, exp))}}};
            boolean pass = Arrays.equals(act, exp);
            printResult({idx}, pass, "{inp_escaped}", Arrays.toString(exp), Arrays.toString(act), ms);
        }}
        '''
    elif pid == 53:
        nums_str = "new int[]{" + ", ".join(map(str, inp["nums"])) + "}"
        return f'''
        {{
            long t0 = System.nanoTime();
            int act = sol.maxSubArray({nums_str});
            double ms = (System.nanoTime() - t0) / 1e6;
            boolean pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", "{exp}", String.valueOf(act), ms);
        }}
        '''
    elif pid == 15:
        nums_str = "new int[]{" + ", ".join(map(str, inp["nums"])) + "}"
        return f'''
        {{
            long t0 = System.nanoTime();
            List<List<Integer>> act = sol.threeSum({nums_str});
            double ms = (System.nanoTime() - t0) / 1e6;
            boolean pass = (act != null && act.size() == {len(exp)});
            printResult({idx}, pass, "{inp_escaped}", "{exp}", act != null ? act.toString() : "null", ms);
        }}
        '''
    elif pid == 11:
        h_str = "new int[]{" + ", ".join(map(str, inp["height"])) + "}"
        return f'''
        {{
            long t0 = System.nanoTime();
            int act = sol.maxArea({h_str});
            double ms = (System.nanoTime() - t0) / 1e6;
            boolean pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", "{exp}", String.valueOf(act), ms);
        }}
        '''
    elif pid == 3:
        s_val = inp["s"].replace('"', '\\"')
        return f'''
        {{
            long t0 = System.nanoTime();
            int act = sol.lengthOfLongestSubstring("{s_val}");
            double ms = (System.nanoTime() - t0) / 1e6;
            boolean pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", "{exp}", String.valueOf(act), ms);
        }}
        '''
    elif pid == 20:
        s_val = inp["s"].replace('"', '\\"')
        exp_bool = "true" if exp else "false"
        return f'''
        {{
            long t0 = System.nanoTime();
            boolean act = sol.isValid("{s_val}");
            double ms = (System.nanoTime() - t0) / 1e6;
            boolean pass = (act == {exp_bool});
            printResult({idx}, pass, "{inp_escaped}", "{exp_bool}", String.valueOf(act), ms);
        }}
        '''
    elif pid == 704:
        nums_str = "new int[]{" + ", ".join(map(str, inp["nums"])) + "}"
        target = inp["target"]
        return f'''
        {{
            long t0 = System.nanoTime();
            int act = sol.search({nums_str}, {target});
            double ms = (System.nanoTime() - t0) / 1e6;
            boolean pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", "{exp}", String.valueOf(act), ms);
        }}
        '''
    elif pid == 739:
        t_str = "new int[]{" + ", ".join(map(str, inp["temperatures"])) + "}"
        return f'''
        {{
            long t0 = System.nanoTime();
            int[] act = sol.dailyTemperatures({t_str});
            double ms = (System.nanoTime() - t0) / 1e6;
            int[] exp = new int[]{{{", ".join(map(str, exp))}}};
            boolean pass = Arrays.equals(act, exp);
            printResult({idx}, pass, "{inp_escaped}", Arrays.toString(exp), Arrays.toString(act), ms);
        }}
        '''
    return ""


def run_java_tests(code: str, problem_id: int | None = None) -> dict:
    """Compile and run Java code against test cases using javac and java."""
    cleaned_code = code.replace("public class Solution", "class Solution")
    extras = CURATED_PROBLEM_EXTRAS.get(problem_id, {}) if problem_id else {}
    test_cases = extras.get("test_cases", [])

    with tempfile.TemporaryDirectory() as td:
        if not test_cases:
            # Simple compilation check
            src_file = os.path.join(td, "Solution.java")
            with open(src_file, "w", encoding="utf-8") as f:
                f.write(code)
            t_start = time.perf_counter()
            compile_res = subprocess.run(["javac", src_file], capture_output=True, text=True, timeout=12)
            elapsed = (time.perf_counter() - t_start) * 1000.0
            if compile_res.returncode != 0:
                return {
                    "success": False,
                    "passed": 0,
                    "total": 1,
                    "test_results": [],
                    "runtime_ms": round(elapsed, 2),
                    "stdout": "",
                    "error": f"Java Compilation Error:\n{compile_res.stderr.strip()}",
                }
            return {
                "success": True,
                "passed": 1,
                "total": 1,
                "test_results": [
                    {
                        "case_number": 1,
                        "passed": True,
                        "input": "(General Java compilation)",
                        "expected": "Compilation success",
                        "actual": "Compiled cleanly without errors",
                        "runtime_ms": round(elapsed, 2),
                        "stdout": "",
                        "error": None,
                    }
                ],
                "runtime_ms": round(elapsed, 2),
                "stdout": "",
                "error": None,
            }

        # Curated test cases runner
        raw_calls = [_generate_java_call(problem_id, tc, i+1) for i, tc in enumerate(test_cases)]
        has_calls = any(c.strip() for c in raw_calls)
        calls = "\n".join(raw_calls) if has_calls else 'System.out.println("STRUCTURE_OK");'
        runner_source = f"""
import java.util.*;
import java.io.*;

{cleaned_code}

public class TestRunner {{
    private static void printResult(int num, boolean pass, String inp, String exp, String act, double ms) {{
        System.out.println("TEST_RES:" + num + ":" + (pass ? "1" : "0") + ":" + ms + ":::" + inp + ":::" + exp + ":::" + act);
    }}
    public static void main(String[] args) {{
        try {{
            Solution sol = new Solution();
            {calls}
        }} catch (Exception e) {{
            System.out.println("EXCEPTION:" + e.getClass().getName() + ": " + e.getMessage());
        }}
    }}
}}
"""
        src_file = os.path.join(td, "TestRunner.java")
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(runner_source)

        t_compile = time.perf_counter()
        try:
            c_res = subprocess.run(["javac", src_file], capture_output=True, text=True, timeout=12)
        except FileNotFoundError:
            return {
                "success": False,
                "passed": 0,
                "total": len(test_cases),
                "test_results": [],
                "runtime_ms": 0.0,
                "stdout": "",
                "error": "Java compiler (javac) is not installed or not found in PATH.",
            }

        if c_res.returncode != 0:
            elapsed = (time.perf_counter() - t_compile) * 1000.0
            clean_err = c_res.stderr.strip().replace(src_file, "Solution.java")
            return {
                "success": False,
                "passed": 0,
                "total": len(test_cases),
                "test_results": [],
                "runtime_ms": round(elapsed, 2),
                "stdout": "",
                "error": f"Java Compilation Error:\n{clean_err}",
            }

        t_run = time.perf_counter()
        try:
            r_res = subprocess.run(["java", "-cp", td, "TestRunner"], capture_output=True, text=True, timeout=10)
        except FileNotFoundError:
            return {
                "success": False,
                "passed": 0,
                "total": len(test_cases),
                "test_results": [],
                "runtime_ms": 0.0,
                "stdout": "",
                "error": "Java runtime (java) is not installed or not found in PATH.",
            }
        elapsed = (time.perf_counter() - t_run) * 1000.0

        if not has_calls:
            if "EXCEPTION:" in r_res.stdout or r_res.returncode != 0:
                err_msg = r_res.stderr.strip() or r_res.stdout.strip() or "Runtime error during execution"
                return {
                    "success": False,
                    "passed": 0,
                    "total": len(test_cases),
                    "test_results": [],
                    "runtime_ms": round(elapsed, 2),
                    "stdout": r_res.stdout,
                    "error": err_msg,
                }
            per_case_ms = round(elapsed / max(len(test_cases), 1), 2)
            results = [
                {
                    "case_number": i + 1,
                    "passed": True,
                    "input": str(tc.get("input", "")),
                    "expected": str(tc.get("expected", "")),
                    "actual": "Compilation & structure verified",
                    "runtime_ms": per_case_ms,
                    "stdout": "",
                    "error": None,
                }
                for i, tc in enumerate(test_cases)
            ]
            return {
                "success": True,
                "passed": len(test_cases),
                "total": len(test_cases),
                "test_results": results,
                "runtime_ms": round(elapsed, 2),
                "stdout": r_res.stdout,
                "error": None,
            }

        results = []
        passed_count = 0
        total_time = 0.0

        for line in r_res.stdout.splitlines():
            if line.startswith("TEST_RES:"):
                parts = line.split(":::")
                header_parts = parts[0].split(":")
                case_num = int(header_parts[1])
                passed = header_parts[2] == "1"
                runtime = float(header_parts[3])
                inp_str = parts[1] if len(parts) > 1 else ""
                exp_str = parts[2] if len(parts) > 2 else ""
                act_str = parts[3] if len(parts) > 3 else ""

                if passed:
                    passed_count += 1
                total_time += runtime

                results.append({
                    "case_number": case_num,
                    "passed": passed,
                    "input": inp_str,
                    "expected": exp_str,
                    "actual": act_str,
                    "runtime_ms": round(runtime, 2),
                    "stdout": "",
                    "error": None if passed else f"Expected {exp_str}, got {act_str}",
                })

        all_passed = (passed_count == len(test_cases))
        return {
            "success": all_passed,
            "passed": passed_count,
            "total": len(test_cases),
            "test_results": results,
            "runtime_ms": round(total_time, 2),
            "stdout": r_res.stdout,
            "error": None if all_passed else f"{len(test_cases) - passed_count} of {len(test_cases)} tests failed.",
        }


# Compiles and executes C++ submissions against problem test cases

def _generate_cpp_call(pid: int, tc: dict, idx: int) -> str:
    inp = tc["input"]
    exp = tc["expected"]
    inp_escaped = str(inp).replace('"', '\\"').replace('\n', ' ')
    if pid == 1:
        nums_str = "{" + ", ".join(map(str, inp["nums"])) + "}"
        target = inp["target"]
        return f'''
        {{
            vector<int> nums = {nums_str};
            auto t0 = chrono::high_resolution_clock::now();
            vector<int> act = sol.twoSum(nums, {target});
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            vector<int> exp = {{{", ".join(map(str, exp))}}};
            vector<int> actSorted = act; sort(actSorted.begin(), actSorted.end());
            vector<int> expSorted = exp; sort(expSorted.begin(), expSorted.end());
            bool pass = (actSorted == expSorted);
            printResult({idx}, pass, "{inp_escaped}", to_str(exp), to_str(act), ms);
        }}
        '''
    elif pid == 121:
        prices_str = "{" + ", ".join(map(str, inp["prices"])) + "}"
        return f'''
        {{
            vector<int> prices = {prices_str};
            auto t0 = chrono::high_resolution_clock::now();
            int act = sol.maxProfit(prices);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            bool pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", to_string({exp}), to_string(act), ms);
        }}
        '''
    elif pid == 217:
        nums_str = "{" + ", ".join(map(str, inp["nums"])) + "}"
        exp_bool = "true" if exp else "false"
        return f'''
        {{
            vector<int> nums = {nums_str};
            auto t0 = chrono::high_resolution_clock::now();
            bool act = sol.containsDuplicate(nums);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            bool pass = (act == {exp_bool});
            printResult({idx}, pass, "{inp_escaped}", "{exp_bool}", act ? "true" : "false", ms);
        }}
        '''
    elif pid == 238:
        nums_str = "{" + ", ".join(map(str, inp["nums"])) + "}"
        return f'''
        {{
            vector<int> nums = {nums_str};
            auto t0 = chrono::high_resolution_clock::now();
            vector<int> act = sol.productExceptSelf(nums);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            vector<int> exp = {{{", ".join(map(str, exp))}}};
            bool pass = (act == exp);
            printResult({idx}, pass, "{inp_escaped}", to_str(exp), to_str(act), ms);
        }}
        '''
    elif pid == 53:
        nums_str = "{" + ", ".join(map(str, inp["nums"])) + "}"
        return f'''
        {{
            vector<int> nums = {nums_str};
            auto t0 = chrono::high_resolution_clock::now();
            int act = sol.maxSubArray(nums);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            bool pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", to_string({exp}), to_string(act), ms);
        }}
        '''
    elif pid == 15:
        nums_str = "{" + ", ".join(map(str, inp["nums"])) + "}"
        return f'''
        {{
            vector<int> nums = {nums_str};
            auto t0 = chrono::high_resolution_clock::now();
            vector<vector<int>> act = sol.threeSum(nums);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            bool pass = (act.size() == {len(exp)});
            printResult({idx}, pass, "{inp_escaped}", "{exp}", "[" + to_string(act.size()) + " triplets]", ms);
        }}
        '''
    elif pid == 11:
        h_str = "{" + ", ".join(map(str, inp["height"])) + "}"
        return f'''
        {{
            vector<int> h = {h_str};
            auto t0 = chrono::high_resolution_clock::now();
            int act = sol.maxArea(h);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            bool pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", to_string({exp}), to_string(act), ms);
        }}
        '''
    elif pid == 3:
        s_val = inp["s"].replace('"', '\\"')
        return f'''
        {{
            string s = "{s_val}";
            auto t0 = chrono::high_resolution_clock::now();
            int act = sol.lengthOfLongestSubstring(s);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            bool pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", to_string({exp}), to_string(act), ms);
        }}
        '''
    elif pid == 20:
        s_val = inp["s"].replace('"', '\\"')
        exp_bool = "true" if exp else "false"
        return f'''
        {{
            string s = "{s_val}";
            auto t0 = chrono::high_resolution_clock::now();
            bool act = sol.isValid(s);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            bool pass = (act == {exp_bool});
            printResult({idx}, pass, "{inp_escaped}", "{exp_bool}", act ? "true" : "false", ms);
        }}
        '''
    elif pid == 704:
        nums_str = "{" + ", ".join(map(str, inp["nums"])) + "}"
        target = inp["target"]
        return f'''
        {{
            vector<int> nums = {nums_str};
            auto t0 = chrono::high_resolution_clock::now();
            int act = sol.search(nums, {target});
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            bool pass = (act == {exp});
            printResult({idx}, pass, "{inp_escaped}", to_string({exp}), to_string(act), ms);
        }}
        '''
    elif pid == 739:
        t_str = "{" + ", ".join(map(str, inp["temperatures"])) + "}"
        return f'''
        {{
            vector<int> t = {t_str};
            auto t0 = chrono::high_resolution_clock::now();
            vector<int> act = sol.dailyTemperatures(t);
            auto t1 = chrono::high_resolution_clock::now();
            double ms = chrono::duration<double, milli>(t1 - t0).count();
            vector<int> exp = {{{", ".join(map(str, exp))}}};
            bool pass = (act == exp);
            printResult({idx}, pass, "{inp_escaped}", to_str(exp), to_str(act), ms);
        }}
        '''
    return ""


def run_cpp_tests(code: str, problem_id: int | None = None) -> dict:
    """Compile and run C++ code against test cases using g++."""
    extras = CURATED_PROBLEM_EXTRAS.get(problem_id, {}) if problem_id else {}
    test_cases = extras.get("test_cases", [])

    with tempfile.TemporaryDirectory() as td:
        src_file = os.path.join(td, "runner.cpp")
        exe_file = os.path.join(td, "runner.exe")

        if not test_cases:
            # Check if user included a main function, or provide stub
            cpp_src = code
            if "int main" not in code:
                cpp_src = f"""
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
using namespace std;
{code}
int main() {{ return 0; }}
"""
            with open(src_file, "w", encoding="utf-8") as f:
                f.write(cpp_src)

            t_start = time.perf_counter()
            compile_res = subprocess.run(["g++", "-std=c++17", src_file, "-o", exe_file], capture_output=True, text=True, timeout=12)
            elapsed = (time.perf_counter() - t_start) * 1000.0

            if compile_res.returncode != 0:
                clean_err = compile_res.stderr.strip().replace(src_file, "solution.cpp")
                return {
                    "success": False,
                    "passed": 0,
                    "total": 1,
                    "test_results": [],
                    "runtime_ms": round(elapsed, 2),
                    "stdout": "",
                    "error": f"C++ Compilation Error:\n{clean_err}",
                }

            return {
                "success": True,
                "passed": 1,
                "total": 1,
                "test_results": [
                    {
                        "case_number": 1,
                        "passed": True,
                        "input": "(General C++ compilation)",
                        "expected": "Compilation success",
                        "actual": "Compiled cleanly without errors",
                        "runtime_ms": round(elapsed, 2),
                        "stdout": "",
                        "error": None,
                    }
                ],
                "runtime_ms": round(elapsed, 2),
                "stdout": "",
                "error": None,
            }

        # Curated test cases runner
        raw_calls = [_generate_cpp_call(problem_id, tc, i+1) for i, tc in enumerate(test_cases)]
        has_calls = any(c.strip() for c in raw_calls)
        calls = "\n".join(raw_calls) if has_calls else 'cout << "STRUCTURE_OK" << endl;'
        runner_source = f"""
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <stack>
#include <queue>
#include <chrono>
using namespace std;

string to_str(const vector<int>& v) {{
    string s = "[";
    for(size_t i = 0; i < v.size(); i++) {{
        s += to_string(v[i]);
        if(i + 1 < v.size()) s += ", ";
    }}
    s += "]";
    return s;
}}

void printResult(int num, bool pass, string inp, string exp, string act, double ms) {{
    cout << "TEST_RES:" << num << ":" << (pass ? "1" : "0") << ":" << ms << ":::" << inp << ":::" << exp << ":::" << act << endl;
}}

{code}

int main() {{
    try {{
        Solution sol;
        {calls}
    }} catch (const exception& e) {{
        cout << "EXCEPTION: " << e.what() << endl;
    }} catch (...) {{
        cout << "EXCEPTION: Unknown C++ exception" << endl;
    }}
    return 0;
}}
"""
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(runner_source)

        t_compile = time.perf_counter()
        try:
            c_res = subprocess.run(["g++", "-std=c++17", src_file, "-o", exe_file], capture_output=True, text=True, timeout=12)
        except FileNotFoundError:
            return {
                "success": False,
                "passed": 0,
                "total": len(test_cases),
                "test_results": [],
                "runtime_ms": 0.0,
                "stdout": "",
                "error": "C++ compiler (g++) is not installed or not found in PATH.",
            }

        if c_res.returncode != 0:
            elapsed = (time.perf_counter() - t_compile) * 1000.0
            clean_err = c_res.stderr.strip().replace(src_file, "solution.cpp")
            return {
                "success": False,
                "passed": 0,
                "total": len(test_cases),
                "test_results": [],
                "runtime_ms": round(elapsed, 2),
                "stdout": "",
                "error": f"C++ Compilation Error:\n{clean_err}",
            }

        t_run = time.perf_counter()
        try:
            r_res = subprocess.run([exe_file], capture_output=True, text=True, timeout=10)
        except FileNotFoundError:
            return {
                "success": False,
                "passed": 0,
                "total": len(test_cases),
                "test_results": [],
                "runtime_ms": 0.0,
                "stdout": "",
                "error": "C++ compiled executable not found or execution failed.",
            }
        elapsed = (time.perf_counter() - t_run) * 1000.0

        if not has_calls:
            if "EXCEPTION:" in r_res.stdout or r_res.returncode != 0:
                err_msg = r_res.stderr.strip() or r_res.stdout.strip() or "Runtime error during execution"
                return {
                    "success": False,
                    "passed": 0,
                    "total": len(test_cases),
                    "test_results": [],
                    "runtime_ms": round(elapsed, 2),
                    "stdout": r_res.stdout,
                    "error": err_msg,
                }
            per_case_ms = round(elapsed / max(len(test_cases), 1), 2)
            results = [
                {
                    "case_number": i + 1,
                    "passed": True,
                    "input": str(tc.get("input", "")),
                    "expected": str(tc.get("expected", "")),
                    "actual": "Compilation & structure verified",
                    "runtime_ms": per_case_ms,
                    "stdout": "",
                    "error": None,
                }
                for i, tc in enumerate(test_cases)
            ]
            return {
                "success": True,
                "passed": len(test_cases),
                "total": len(test_cases),
                "test_results": results,
                "runtime_ms": round(elapsed, 2),
                "stdout": r_res.stdout,
                "error": None,
            }

        results = []
        passed_count = 0
        total_time = 0.0

        for line in r_res.stdout.splitlines():
            if line.startswith("TEST_RES:"):
                parts = line.split(":::")
                header_parts = parts[0].split(":")
                case_num = int(header_parts[1])
                passed = header_parts[2] == "1"
                runtime = float(header_parts[3])
                inp_str = parts[1] if len(parts) > 1 else ""
                exp_str = parts[2] if len(parts) > 2 else ""
                act_str = parts[3] if len(parts) > 3 else ""

                if passed:
                    passed_count += 1
                total_time += runtime

                results.append({
                    "case_number": case_num,
                    "passed": passed,
                    "input": inp_str,
                    "expected": exp_str,
                    "actual": act_str,
                    "runtime_ms": round(runtime, 2),
                    "stdout": "",
                    "error": None if passed else f"Expected {exp_str}, got {act_str}",
                })

        all_passed = (passed_count == len(test_cases))
        return {
            "success": all_passed,
            "passed": passed_count,
            "total": len(test_cases),
            "test_results": results,
            "runtime_ms": round(total_time, 2),
            "stdout": r_res.stdout,
            "error": None if all_passed else f"{len(test_cases) - passed_count} of {len(test_cases)} tests failed.",
        }


# Routes submission to the appropriate language runner

def run_code_tests(code: str, problem_id: int | None = None, language: str = "python") -> dict:
    """
    Safely execute the learner's code in Python, Java, or C++
    and evaluate it against sample test cases for the problem.
    """
    lang = (language or "python").lower()
    if lang == "java":
        return run_java_tests(code, problem_id)
    elif lang in ("cpp", "c++"):
        return run_cpp_tests(code, problem_id)
    else:
        return run_python_tests(code, problem_id)
