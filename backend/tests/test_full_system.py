import pytest
from starlette.testclient import TestClient

from app.main import app
from app.analyzer.analyzer import analyze_code
from app.runner import run_code_tests


client = TestClient(app)


def test_two_pointers_detection():
    code = """
class Solution:
    def maxArea(self, height):
        left = 0
        right = len(height) - 1
        max_area = 0
        while left < right:
            h = min(height[left], height[right])
            max_area = max(max_area, h * (right - left))
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area
"""
    result = analyze_code(code, problem_id=11)
    assert result["syntax_valid"] is True
    assert result["features"]["has_two_pointers"] is True
    assert result["pattern"]["name"] == "two_pointers"
    assert result["complexity"]["time"] == "O(n)"
    assert result["complexity"]["space"] == "O(1)"
    assert result["complexity"]["efficiency_rating"] == "Optimal Time"


def test_sliding_window_detection():
    code = """
class Solution:
    def lengthOfLongestSubstring(self, s):
        seen = set()
        left = 0
        max_len = 0
        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            max_len = max(max_len, right - left + 1)
        return max_len
"""
    result = analyze_code(code, problem_id=3)
    assert result["syntax_valid"] is True
    assert result["features"]["has_sliding_window"] is True
    assert result["pattern"]["name"] == "sliding_window"
    assert result["complexity"]["time"] == "O(n)"


def test_binary_search_detection():
    code = """
class Solution:
    def search(self, nums, target):
        low = 0
        high = len(nums) - 1
        while low <= high:
            mid = (low + high) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1
"""
    result = analyze_code(code, problem_id=704)
    assert result["syntax_valid"] is True
    assert result["features"]["has_binary_search"] is True
    assert result["pattern"]["name"] == "binary_search"
    assert result["complexity"]["time"] == "O(log n)"


def test_kadane_detection():
    code = """
class Solution:
    def maxSubArray(self, nums):
        current_sum = max_sum = nums[0]
        for x in nums[1:]:
            current_sum = max(x, current_sum + x)
            max_sum = max(max_sum, current_sum)
        return max_sum
"""
    result = analyze_code(code, problem_id=53)
    assert result["syntax_valid"] is True
    assert result["pattern"]["name"] == "kadane"
    assert result["complexity"]["time"] == "O(n)"


def test_monotonic_stack_detection():
    code = """
class Solution:
    def dailyTemperatures(self, temperatures):
        stack = []
        res = [0] * len(temperatures)
        for i, t in enumerate(temperatures):
            while stack and t > temperatures[stack[-1]]:
                prev_i = stack.pop()
                res[prev_i] = i - prev_i
            stack.append(i)
        return res
"""
    result = analyze_code(code, problem_id=739)
    assert result["syntax_valid"] is True
    assert result["features"]["has_monotonic_stack"] is True
    assert result["pattern"]["name"] == "monotonic_stack"


def test_code_runner_passing_two_sum():
    code = """
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in seen:
                return [seen[diff], i]
            seen[num] = i
        return []
"""
    result = run_code_tests(code, problem_id=1)
    assert result["success"] is True
    assert result["passed"] == result["total"]
    assert result["total"] >= 3
    assert result["error"] is None


def test_code_runner_failing_two_sum():
    code = """
class Solution:
    def twoSum(self, nums, target):
        return [0, 0]
"""
    result = run_code_tests(code, problem_id=1)
    assert result["success"] is False
    assert result["passed"] < result["total"]


def test_rest_api_endpoints():
    # Health
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    # Problems list
    res = client.get("/problems")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 75

    # Filter problems by category
    res = client.get("/problems?category=Two%20Pointers")
    assert res.status_code == 200
    assert len(res.json()["problems"]) > 0

    # Problem details
    res = client.get("/problems/1")
    assert res.status_code == 200
    p = res.json()
    assert p["title"] == "Two Sum"
    assert "starter_code" in p
    assert "test_cases" in p

    # Analyze endpoint
    res = client.post("/analyze", json={
        "code": "class Solution:\n    def twoSum(self, nums, target):\n        return []",
        "problem_id": 1,
        "hint_level": 1
    })
    assert res.status_code == 200
    analysis = res.json()
    assert analysis["syntax_valid"] is True
    assert "features" in analysis
    assert "pattern" in analysis
    assert "complexity" in analysis
    assert "hints" in analysis

    # Run endpoint
    res = client.post("/run", json={
        "code": "class Solution:\n    def twoSum(self, nums, target):\n        seen = {}\n        for i, x in enumerate(nums):\n            if target - x in seen: return [seen[target - x], i]\n            seen[x] = i\n        return []",
        "problem_id": 1
    })
    assert res.status_code == 200
    assert res.json()["success"] is True


def test_websocket_live_analysis():
    with client.websocket_connect("/ws/analyze") as websocket:
        code = """
class Solution:
    def containsDuplicate(self, nums):
        seen = set()
        for x in nums:
            if x in seen:
                return True
            seen.add(x)
        return False
"""
        websocket.send_json({"code": code, "problem_id": 217, "hint_level": 2})
        data = websocket.receive_json()
        assert data["syntax_valid"] is True
        assert data["features"]["uses_set"] is True
        assert data["pattern"]["name"] == "hash_set"
        assert data["complexity"]["time"] == "O(n)"


def test_java_analysis_brute_force_and_hash_map():
    # Java Brute Force
    java_brute = """
class Solution {
    public int[] twoSum(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[0];
    }
}
"""
    res = client.post("/analyze", json={"code": java_brute, "language": "java", "problem_id": 1})
    assert res.status_code == 200
    data = res.json()
    assert data["syntax_valid"] is True
    assert data["pattern"]["name"] == "brute_force"
    assert data["complexity"]["time"] == "O(n^2)"

    # Java Hash Map
    java_hash_map = """
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (seen.containsKey(need)) {
                return new int[]{seen.get(need), i};
            }
            seen.put(nums[i], i);
        }
        return new int[0];
    }
}
"""
    res = client.post("/analyze", json={"code": java_hash_map, "language": "java", "problem_id": 1})
    assert res.status_code == 200
    data = res.json()
    assert data["syntax_valid"] is True
    assert data["features"]["uses_dictionary"] is True
    assert data["pattern"]["name"] == "hash_map"
    assert data["complexity"]["time"] == "O(n)"


def test_cpp_analysis_two_pointers():
    cpp_two_pointers = """
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxArea(vector<int>& height) {
        int left = 0, right = height.size() - 1;
        int max_area = 0;
        while (left < right) {
            int h = min(height[left], height[right]);
            max_area = max(max_area, h * (right - left));
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return max_area;
    }
};
"""
    res = client.post("/analyze", json={"code": cpp_two_pointers, "language": "cpp", "problem_id": 11})
    assert res.status_code == 200
    data = res.json()
    assert data["syntax_valid"] is True
    assert data["features"]["has_two_pointers"] is True
    assert data["pattern"]["name"] == "two_pointers"
    assert data["complexity"]["time"] == "O(n)"

