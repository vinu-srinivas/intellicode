import json

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for p in db["problems"]:
    if p["leetcode_id"] == 53:
        p["primary_approach"] = "Kadane"
        p["primary_solution"]["approach"] = "Kadane"
        
        kadane_py = """class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_so_far = nums[0]
        current_sum = nums[0]
        for i in range(1, len(nums)):
            current_sum = max(nums[i], current_sum + nums[i])
            max_so_far = max(max_so_far, current_sum)
        return max_so_far
"""
        kadane_java = """class Solution {
    public int maxSubArray(int[] nums) {
        int maxSoFar = nums[0];
        int currentSum = nums[0];
        for (int i = 1; i < nums.length; i++) {
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSoFar = Math.max(maxSoFar, currentSum);
        }
        return maxSoFar;
    }
}
"""
        kadane_cpp = """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        int maxSoFar = nums[0];
        int currentSum = nums[0];
        for (size_t i = 1; i < nums.size(); i++) {
            currentSum = max(nums[i], currentSum + nums[i]);
            maxSoFar = max(maxSoFar, currentSum);
        }
        return maxSoFar;
    }
};
"""
        p["primary_solution"]["code"]["python"] = kadane_py
        p["primary_solution"]["code"]["java"] = kadane_java
        p["primary_solution"]["code"]["cpp"] = kadane_cpp
        
        for a in p["approaches"]:
            if a["name"] == "Kadane":
                a["code"]["python"] = kadane_py
                a["code"]["java"] = kadane_java
                a["code"]["cpp"] = kadane_cpp

with open("codebase.json", "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Fixed Problem 53 Kadane codes.")
