CHUNK_2 = {
    73: {
        "description": "Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.\n\nYou must do it in place.",
        "examples": [
            {"input": "matrix = [[1,1,1],[1,0,1],[1,1,1]]", "output": "[[1,0,1],[0,0,0],[1,0,1]]"},
            {"input": "matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "output": "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]"}
        ],
        "constraints": [
            "m == matrix.length",
            "n == matrix[0].length",
            "1 <= m, n <= 200",
            "-2^31 <= matrix[i][j] <= 2^31 - 1"
        ],
        "test_cases": [
            {"input": {"matrix": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]}, "expected": [[1, 0, 1], [0, 0, 0], [1, 0, 1]]},
            {"input": {"matrix": [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]}, "expected": [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def setZeroes(self, matrix: List[List[int]]) -> None:\n        \"\"\"\n        Do not return anything, modify matrix in-place instead.\n        \"\"\"\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public void setZeroes(int[][] matrix) {\n        // Write your solution here\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    void setZeroes(vector<vector<int>>& matrix) {\n        // Write your solution here\n    }\n};\n"
        }
    },
    54: {
        "description": "Given an m x n matrix, return all elements of the matrix in spiral order.",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[1,2,3,6,9,8,7,4,5]"},
            {"input": "matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "output": "[1,2,3,4,8,12,11,10,9,5,6,7]"}
        ],
        "constraints": [
            "m == matrix.length",
            "n == matrix[i].length",
            "1 <= m, n <= 10",
            "-100 <= matrix[i][j] <= 100"
        ],
        "test_cases": [
            {"input": {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, "expected": [1, 2, 3, 6, 9, 8, 7, 4, 5]},
            {"input": {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]}, "expected": [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<Integer> spiralOrder(int[][] matrix) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> spiralOrder(vector<vector<int>>& matrix) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        }
    },
    48: {
        "description": "You are given an n x n 2D matrix representing an image, rotate the image by 90 degrees (clockwise).\n\nYou have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.",
        "examples": [
            {"input": "matrix = [[1,2,3],[4,5,6],[7,8,9]]", "output": "[[7,4,1],[8,5,2],[9,6,3]]"},
            {"input": "matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]", "output": "[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]"}
        ],
        "constraints": [
            "n == matrix.length == matrix[i].length",
            "1 <= n <= 20",
            "-1000 <= matrix[i][j] <= 1000"
        ],
        "test_cases": [
            {"input": {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, "expected": [[7, 4, 1], [8, 5, 2], [9, 6, 3]]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def rotate(self, matrix: List[List[int]]) -> None:\n        \"\"\"\n        Do not return anything, modify matrix in-place instead.\n        \"\"\"\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public void rotate(int[][] matrix) {\n        // Write your solution here\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    void rotate(vector<vector<int>>& matrix) {\n        // Write your solution here\n    }\n};\n"
        }
    },
    189: {
        "description": "Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.",
        "examples": [
            {"input": "nums = [1,2,3,4,5,6,7], k = 3", "output": "[5,6,7,1,2,3,4]", "explanation": "rotate 1 steps to the right: [7,1,2,3,4,5,6]\nrotate 2 steps to the right: [6,7,1,2,3,4,5]\nrotate 3 steps to the right: [5,6,7,1,2,3,4]"},
            {"input": "nums = [-1,-100,3,99], k = 2", "output": "[3,99,-1,-100]"}
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-2^31 <= nums[i] <= 2^31 - 1",
            "0 <= k <= 10^5"
        ],
        "test_cases": [
            {"input": {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3}, "expected": [5, 6, 7, 1, 2, 3, 4]},
            {"input": {"nums": [-1, -100, 3, 99], "k": 2}, "expected": [3, 99, -1, -100]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def rotate(self, nums: List[int], k: int) -> None:\n        \"\"\"\n        Do not return anything, modify nums in-place instead.\n        \"\"\"\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public void rotate(int[] nums, int k) {\n        // Write your solution here\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    void rotate(vector<int>& nums, int k) {\n        // Write your solution here\n    }\n};\n"
        }
    },
    41: {
        "description": "Given an unsorted integer array nums. Return the smallest positive integer that is not present in nums.\n\nYou must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.",
        "examples": [
            {"input": "nums = [1,2,0]", "output": "3", "explanation": "The numbers in the range [1,2] are all in the array."},
            {"input": "nums = [3,4,-1,1]", "output": "2", "explanation": "1 is in the array but 2 is missing."},
            {"input": "nums = [7,8,9,11,12]", "output": "1", "explanation": "The smallest positive integer 1 is missing."}
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-2^31 <= nums[i] <= 2^31 - 1"
        ],
        "test_cases": [
            {"input": {"nums": [1, 2, 0]}, "expected": 3},
            {"input": {"nums": [3, 4, -1, 1]}, "expected": 2},
            {"input": {"nums": [7, 8, 9, 11, 12]}, "expected": 1},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def firstMissingPositive(self, nums: List[int]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int firstMissingPositive(int[] nums) {\n        // Write your solution here\n        return 1;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int firstMissingPositive(vector<int>& nums) {\n        // Write your solution here\n        return 1;\n    }\n};\n"
        }
    },
    3: {
        "description": "Given a string s, find the length of the longest substring without repeating characters.",
        "examples": [
            {"input": "s = \"abcabcbb\"", "output": "3", "explanation": "The answer is \"abc\", with the length of 3."},
            {"input": "s = \"bbbbb\"", "output": "1", "explanation": "The answer is \"b\", with the length of 1."},
            {"input": "s = \"pwwkew\"", "output": "3", "explanation": "The answer is \"wke\", with the length of 3."}
        ],
        "constraints": [
            "0 <= s.length <= 5 * 10^4",
            "s consists of English letters, digits, symbols and spaces."
        ],
        "test_cases": [
            {"input": {"s": "abcabcbb"}, "expected": 3},
            {"input": {"s": "bbbbb"}, "expected": 1},
            {"input": {"s": "pwwkew"}, "expected": 3},
            {"input": {"s": ""}, "expected": 0},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def lengthOfLongestSubstring(self, s: str) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int lengthOfLongestSubstring(String s) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int lengthOfLongestSubstring(string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    424: {
        "description": "You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.\n\nReturn the length of the longest substring containing the same letter you can get after performing the above operations.",
        "examples": [
            {"input": "s = \"ABAB\", k = 2", "output": "4", "explanation": "Replace the two 'A's with two 'B's or vice versa."},
            {"input": "s = \"AABABBA\", k = 1", "output": "4", "explanation": "Replace the one 'A' in the middle with 'B' and form \"AABBBBA\"."}
        ],
        "constraints": [
            "1 <= s.length <= 10^5",
            "s consists of only uppercase English letters.",
            "0 <= k <= s.length"
        ],
        "test_cases": [
            {"input": {"s": "ABAB", "k": 2}, "expected": 4},
            {"input": {"s": "AABABBA", "k": 1}, "expected": 4},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def characterReplacement(self, s: str, k: int) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int characterReplacement(String s, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int characterReplacement(string s, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    76: {
        "description": "Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string \"\".",
        "examples": [
            {"input": "s = \"ADOBECODEBANC\", t = \"ABC\"", "output": "\"BANC\"", "explanation": "The minimum window substring \"BANC\" includes 'A', 'B', and 'C' from string t."},
            {"input": "s = \"a\", t = \"a\"", "output": "\"a\""},
            {"input": "s = \"a\", t = \"aa\"", "output": "\"\"", "explanation": "Both 'a's from t must be included in the window."}
        ],
        "constraints": [
            "m == s.length",
            "n == t.length",
            "1 <= m, n <= 10^5",
            "s and t consist of uppercase and lowercase English letters."
        ],
        "test_cases": [
            {"input": {"s": "ADOBECODEBANC", "t": "ABC"}, "expected": "BANC"},
            {"input": {"s": "a", "t": "a"}, "expected": "a"},
            {"input": {"s": "a", "t": "aa"}, "expected": ""},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def minWindow(self, s: str, t: str) -> str:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public String minWindow(String s, String t) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    string minWindow(string s, string t) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        }
    },
    438: {
        "description": "Given two strings s and p, return an array of all the start indices of p's anagrams in s. You may return the answer in any order.",
        "examples": [
            {"input": "s = \"cbaebabacd\", p = \"abc\"", "output": "[0,6]", "explanation": "The substring with start index = 0 is \"cba\", which is an anagram of \"abc\". The substring with start index = 6 is \"bac\", which is an anagram of \"abc\"."},
            {"input": "s = \"abab\", p = \"ab\"", "output": "[0,1,2]"}
        ],
        "constraints": [
            "1 <= s.length, p.length <= 3 * 10^4",
            "s and p consist of lowercase English letters."
        ],
        "test_cases": [
            {"input": {"s": "cbaebabacd", "p": "abc"}, "expected": [0, 6]},
            {"input": {"s": "abab", "p": "ab"}, "expected": [0, 1, 2]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def findAnagrams(self, s: str, p: str) -> List[int]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<Integer> findAnagrams(String s, String p) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> findAnagrams(string s, string p) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        }
    },
    567: {
        "description": "Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.\n\nIn other words, return true if one of s1's permutations is the substring of s2.",
        "examples": [
            {"input": "s1 = \"ab\", s2 = \"eidbaooo\"", "output": "true", "explanation": "s2 contains one permutation of s1 (\"ba\")."},
            {"input": "s1 = \"ab\", s2 = \"eidboaoo\"", "output": "false"}
        ],
        "constraints": [
            "1 <= s1.length, s2.length <= 10^4",
            "s1 and s2 consist of lowercase English letters."
        ],
        "test_cases": [
            {"input": {"s1": "ab", "s2": "eidbaooo"}, "expected": True},
            {"input": {"s1": "ab", "s2": "eidboaoo"}, "expected": False},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def checkInclusion(self, s1: str, s2: str) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean checkInclusion(String s1, String s2) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool checkInclusion(string s1, string s2) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    125: {
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.\n\nGiven a string s, return true if it is a palindrome, or false otherwise.",
        "examples": [
            {"input": "s = \"A man, a plan, a canal: Panama\"", "output": "true", "explanation": "\"amanaplanacanalpanama\" is a palindrome."},
            {"input": "s = \"race a car\"", "output": "false", "explanation": "\"raceacar\" is not a palindrome."},
            {"input": "s = \" \"", "output": "true", "explanation": "s is an empty string \"\" after removing non-alphanumeric characters."}
        ],
        "constraints": [
            "1 <= s.length <= 2 * 10^5",
            "s consists only of printable ASCII characters."
        ],
        "test_cases": [
            {"input": {"s": "A man, a plan, a canal: Panama"}, "expected": True},
            {"input": {"s": "race a car"}, "expected": False},
            {"input": {"s": " "}, "expected": True},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean isPalindrome(String s) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isPalindrome(string s) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    5: {
        "description": "Given a string s, return the longest palindromic substring in s.",
        "examples": [
            {"input": "s = \"babad\"", "output": "\"bab\"", "explanation": "\"aba\" is also a valid answer."},
            {"input": "s = \"cbbd\"", "output": "\"bb\""}
        ],
        "constraints": [
            "1 <= s.length <= 1000",
            "s consist of only digits and English letters."
        ],
        "test_cases": [
            {"input": {"s": "babad"}, "expected": "bab"},
            {"input": {"s": "cbbd"}, "expected": "bb"},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def longestPalindrome(self, s: str) -> str:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public String longestPalindrome(String s) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    string longestPalindrome(string s) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        }
    },
    242: {
        "description": "Given two strings s and t, return true if t is an anagram of s, and false otherwise.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "examples": [
            {"input": "s = \"anagram\", t = \"nagaram\"", "output": "true"},
            {"input": "s = \"rat\", t = \"car\"", "output": "false"}
        ],
        "constraints": [
            "1 <= s.length, t.length <= 5 * 10^4",
            "s and t consist of lowercase English letters."
        ],
        "test_cases": [
            {"input": {"s": "anagram", "t": "nagaram"}, "expected": True},
            {"input": {"s": "rat", "t": "car"}, "expected": False},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean isAnagram(String s, String t) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isAnagram(string s, string t) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    20: {
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if open brackets are closed by the same type of brackets, and in the correct order.",
        "examples": [
            {"input": "s = \"()\"", "output": "true"},
            {"input": "s = \"()[]{}\"", "output": "true"},
            {"input": "s = \"(]\"", "output": "false"}
        ],
        "constraints": [
            "1 <= s.length <= 10^4",
            "s consists of parentheses only '()[]{}'."
        ],
        "test_cases": [
            {"input": {"s": "()"}, "expected": True},
            {"input": {"s": "()[]{}"}, "expected": True},
            {"input": {"s": "(]"}, "expected": False},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def isValid(self, s: str) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean isValid(String s) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isValid(string s) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    14: {
        "description": "Write a function to find the longest common prefix string amongst an array of strings.\n\nIf there is no common prefix, return an empty string \"\".",
        "examples": [
            {"input": "strs = [\"flower\",\"flow\",\"flight\"]", "output": "\"fl\""},
            {"input": "strs = [\"dog\",\"racecar\",\"car\"]", "output": "\"\"", "explanation": "There is no common prefix among the input strings."}
        ],
        "constraints": [
            "1 <= strs.length <= 200",
            "0 <= strs[i].length <= 200",
            "strs[i] consists of only lowercase English letters."
        ],
        "test_cases": [
            {"input": {"strs": ["flower", "flow", "flight"]}, "expected": "fl"},
            {"input": {"strs": ["dog", "racecar", "car"]}, "expected": ""},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def longestCommonPrefix(self, strs: List[str]) -> str:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public String longestCommonPrefix(String[] strs) {\n        // Write your solution here\n        return \"\";\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    string longestCommonPrefix(vector<string>& strs) {\n        // Write your solution here\n        return \"\";\n    }\n};\n"
        }
    }
}
