import json
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
codebase_path = PROJECT_ROOT / "codebase.json"

with open(codebase_path, "r", encoding="utf-8") as f:
    data = json.load(f)

FIXES = {
    53: {
        1: "class Solution:\n    def maxSubArray(self, nums):\n        best = current = nums[0]\n        for x in nums[1:]:\n            current = max(x, current + x)\n            best = max(best, current)\n        return best\n"
    },
    160: {
        1: "class Solution:\n    def getIntersectionNode(self, headA, headB):\n        a, b = headA, headB\n        while a is not b:\n            a = a.next if a else headB\n            b = b.next if b else headA\n        return a\n"
    },
    70: {
        1: "class Solution:\n    def climbStairs(self, n: int) -> int:\n        if n <= 2:\n            return n\n        a, b = 1, 2\n        for _ in range(3, n + 1):\n            a, b = b, a + b\n        return b\n"
    },
    198: {
        1: "class Solution:\n    def rob(self, nums):\n        prev2 = prev1 = 0\n        for x in nums:\n            prev2, prev1 = prev1, max(prev1, prev2 + x)\n        return prev1\n"
    }
}

for p in data["problems"]:
    pid = p["leetcode_id"]
    if pid in FIXES:
        for idx, code_str in FIXES[pid].items():
            if idx < len(p["approaches"]):
                p["approaches"][idx]["code"]["python"] = code_str

with open(codebase_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fixed approach 1 for 53, 160, 70, 198.")
