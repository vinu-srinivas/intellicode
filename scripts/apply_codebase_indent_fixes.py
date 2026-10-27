import json
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
codebase_path = PROJECT_ROOT / "codebase.json"

with open(codebase_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Explicit replacements for the broken python snippets
REPLACEMENTS = {
    # Two Sum Brute Force
    1: {
        "approaches": {
            0: "class Solution:\n    def twoSum(self, nums, target):\n        for i in range(len(nums)):\n            for j in range(i + 1, len(nums)):\n                if nums[i] + nums[j] == target:\n                    return [i, j]\n        return []\n"
        }
    },
    # Contains Duplicate Sort & Scan
    217: {
        "approaches": {
            0: "class Solution:\n    def containsDuplicate(self, nums: list[int]) -> bool:\n        nums.sort()\n        for i in range(len(nums) - 1):\n            if nums[i] == nums[i + 1]:\n                return True\n        return False\n"
        }
    },
    # Maximum Subarray
    53: {
        "primary": "class Solution:\n    def maxSubArray(self, nums):\n        best = current = nums[0]\n        for x in nums[1:]:\n            current = max(x, current + x)\n            best = max(best, current)\n        return best\n",
        "approaches": {
            0: "class Solution:\n    def maxSubArray(self, nums):\n        best = current = nums[0]\n        for x in nums[1:]:\n            current = max(x, current + x)\n            best = max(best, current)\n        return best\n"
        }
    },
    # Top K Frequent
    347: {
        "approaches": {
            0: "class Solution:\n    def topKFrequent(self, nums: list[int], k: int) -> list[int]:\n        counts = {}\n        for num in nums:\n            counts[num] = counts.get(num, 0) + 1\n        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)\n        return [item[0] for item in sorted_items[:k]]\n"
        }
    },
    # Intersection of Two Linked Lists
    160: {
        "primary": "class Solution:\n    def getIntersectionNode(self, headA, headB):\n        a, b = headA, headB\n        while a is not b:\n            a = a.next if a else headB\n            b = b.next if b else headA\n        return a\n",
        "approaches": {
            0: "class Solution:\n    def getIntersectionNode(self, headA, headB):\n        a, b = headA, headB\n        while a is not b:\n            a = a.next if a else headB\n            b = b.next if b else headA\n        return a\n"
        }
    },
    # Invert Binary Tree
    226: {
        "primary": "class Solution:\n    def invertTree(self, root):\n        if not root:\n            return None\n        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)\n        return root\n",
        "approaches": {
            0: "class Solution:\n    def invertTree(self, root):\n        if not root:\n            return None\n        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)\n        return root\n"
        }
    },
    # Maximum Depth of Binary Tree
    104: {
        "primary": "class Solution:\n    def maxDepth(self, root):\n        if not root:\n            return 0\n        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))\n",
        "approaches": {
            0: "class Solution:\n    def maxDepth(self, root):\n        if not root:\n            return 0\n        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))\n"
        }
    },
    # Climbing Stairs
    70: {
        "primary": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        if n <= 2:\n            return n\n        a, b = 1, 2\n        for _ in range(3, n + 1):\n            a, b = b, a + b\n        return b\n",
        "approaches": {
            0: "class Solution:\n    def climbStairs(self, n: int) -> int:\n        if n <= 2:\n            return n\n        a, b = 1, 2\n        for _ in range(3, n + 1):\n            a, b = b, a + b\n        return b\n"
        }
    },
    # House Robber
    198: {
        "primary": "class Solution:\n    def rob(self, nums):\n        prev2 = prev1 = 0\n        for x in nums:\n            prev2, prev1 = prev1, max(prev1, prev2 + x)\n        return prev1\n",
        "approaches": {
            0: "class Solution:\n    def rob(self, nums):\n        prev2 = prev1 = 0\n        for x in nums:\n            prev2, prev1 = prev1, max(prev1, prev2 + x)\n        return prev1\n"
        }
    }
}

for p in data["problems"]:
    pid = p["leetcode_id"]
    if pid in REPLACEMENTS:
        r = REPLACEMENTS[pid]
        if "primary" in r:
            p["primary_solution"]["code"]["python"] = r["primary"]
        if "approaches" in r:
            for idx, code_str in r["approaches"].items():
                if idx < len(p["approaches"]):
                    p["approaches"][idx]["code"]["python"] = code_str

with open(codebase_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Applied explicit indentation fixes to codebase.json.")
