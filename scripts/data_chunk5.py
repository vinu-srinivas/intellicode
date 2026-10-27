CHUNK_5 = {
    133: {
        "description": "Given a reference of a node in a connected undirected graph.\n\nReturn a deep copy (clone) of the graph.\n\nEach node in the graph contains a value (int) and a list (List[Node]) of its neighbors.",
        "examples": [
            {"input": "adjList = [[2,4],[1,3],[2,4],[1,3]]", "output": "[[2,4],[1,3],[2,4],[1,3]]", "explanation": "There are 4 nodes in the graph.\n1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).\n2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).\n3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).\n4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3)."},
            {"input": "adjList = [[]]", "output": "[[]]"},
            {"input": "adjList = []", "output": "[]"}
        ],
        "constraints": [
            "The number of nodes in the graph is in the range [0, 100].",
            "1 <= Node.val <= 100",
            "Node.val is unique for each node.",
            "There are no repeated edges and no self-loops in the graph.",
            "The Graph is connected and all nodes can be visited starting from the given node."
        ],
        "test_cases": [
            {"input": {"adjList": [[2, 4], [1, 3], [2, 4], [1, 3]]}, "expected": [[2, 4], [1, 3], [2, 4], [1, 3]]},
            {"input": {"adjList": []}, "expected": []},
        ],
        "starter_codes": {
            "python": "# Definition for a Node.\n# class Node:\n#     def __init__(self, val = 0, neighbors = None):\n#         self.val = val\n#         self.neighbors = neighbors if neighbors is not None else []\nclass Solution:\n    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\n/*\n// Definition for a Node.\nclass Node {\n    public int val;\n    public List<Node> neighbors;\n    public Node() {\n        val = 0;\n        neighbors = new ArrayList<Node>();\n    }\n    public Node(int _val) {\n        val = _val;\n        neighbors = new ArrayList<Node>();\n    }\n    public Node(int _val, ArrayList<Node> _neighbors) {\n        val = _val;\n        neighbors = _neighbors;\n    }\n}\n*/\nclass Solution {\n    public Node cloneGraph(Node node) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\n/*\n// Definition for a Node.\nclass Node {\npublic:\n    int val;\n    vector<Node*> neighbors;\n    Node() {\n        val = 0;\n        neighbors = vector<Node*>();\n    }\n    Node(int _val) {\n        val = _val;\n        neighbors = vector<Node*>();\n    }\n    Node(int _val, vector<Node*> _neighbors) {\n        val = _val;\n        neighbors = _neighbors;\n    }\n};\n*/\nclass Solution {\npublic:\n    Node* cloneGraph(Node* node) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    207: {
        "description": "There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.\n\nFor example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.\n\nReturn true if you can finish all courses. Otherwise, return false.",
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "true", "explanation": "There are a total of 2 courses to take. To take course 1 you should have finished course 0. So it is possible."},
            {"input": "numCourses = 2, prerequisites = [[1,0],[0,1]]", "output": "false", "explanation": "There are a total of 2 courses to take. To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible."}
        ],
        "constraints": [
            "1 <= numCourses <= 2000",
            "0 <= prerequisites.length <= 5000",
            "prerequisites[i].length == 2",
            "0 <= ai, bi < numCourses",
            "All the pairs prerequisites[i] are unique."
        ],
        "test_cases": [
            {"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "expected": True},
            {"input": {"numCourses": 2, "prerequisites": [[1, 0], [0, 1]]}, "expected": False},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean canFinish(int numCourses, int[][] prerequisites) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    210: {
        "description": "There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.\n\nReturn the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.",
        "examples": [
            {"input": "numCourses = 2, prerequisites = [[1,0]]", "output": "[0,1]", "explanation": "There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1]."},
            {"input": "numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]", "output": "[0,2,1,3]", "explanation": "There are a total of 4 courses to take. Both [0,1,2,3] and [0,2,1,3] are valid."}
        ],
        "constraints": [
            "1 <= numCourses <= 2000",
            "0 <= prerequisites.length <= numCourses * (numCourses - 1)",
            "prerequisites[i].length == 2",
            "0 <= ai, bi < numCourses",
            "ai != bi",
            "All the pairs [ai, bi] are distinct."
        ],
        "test_cases": [
            {"input": {"numCourses": 2, "prerequisites": [[1, 0]]}, "expected": [0, 1]},
            {"input": {"numCourses": 4, "prerequisites": [[1, 0], [2, 0], [3, 1], [3, 2]]}, "expected": [0, 1, 2, 3]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int[] findOrder(int numCourses, int[][] prerequisites) {\n        // Write your solution here\n        return new int[0];\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        }
    },
    994: {
        "description": "You are given an m x n grid where each cell can have one of three values:\n- 0 representing an empty cell,\n- 1 representing a fresh orange, or\n- 2 representing a rotten orange.\n\nEvery minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.\n\nReturn the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.",
        "examples": [
            {"input": "grid = [[2,1,1],[1,1,0],[0,1,1]]", "output": "4"},
            {"input": "grid = [[2,1,1],[0,1,1],[1,0,1]]", "output": "-1", "explanation": "The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally."},
            {"input": "grid = [[0,2]]", "output": "0", "explanation": "Since there are already no fresh oranges at minute 0, the answer is just 0."}
        ],
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 <= m, n <= 10",
            "grid[i][j] is 0, 1, or 2."
        ],
        "test_cases": [
            {"input": {"grid": [[2, 1, 1], [1, 1, 0], [0, 1, 1]]}, "expected": 4},
            {"input": {"grid": [[2, 1, 1], [0, 1, 1], [1, 0, 1]]}, "expected": -1},
            {"input": {"grid": [[0, 2]]}, "expected": 0},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def orangesRotting(self, grid: List[List[int]]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int orangesRotting(int[][] grid) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int orangesRotting(vector<vector<int>>& grid) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    417: {
        "description": "There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.\n\nThe island is partitioned into a grid of square cells. You are given an m x n integer matrix heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).\n\nReturn a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.",
        "examples": [
            {"input": "heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", "output": "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]"},
            {"input": "heights = [[1]]", "output": "[[0,0]]"}
        ],
        "constraints": [
            "m == heights.length",
            "n == heights[r].length",
            "1 <= m, n <= 200",
            "0 <= heights[r][c] <= 10^5"
        ],
        "test_cases": [
            {"input": {"heights": [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]}, "expected": [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]},
            {"input": {"heights": [[1]]}, "expected": [[0, 0]]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> pacificAtlantic(int[][] heights) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        }
    },
    785: {
        "description": "There is an undirected graph with n nodes, where each node is numbered between 0 and n - 1. You are given a 2D array graph, where graph[u] is an array of nodes that node u is adjacent to.\n\nA graph is bipartite if the nodes can be partitioned into two independent sets A and B such that every edge in the graph connects a node in set A and a node in set B.\n\nReturn true if and only if it is bipartite.",
        "examples": [
            {"input": "graph = [[1,2,3],[0,2],[0,1,3],[0,2]]", "output": "false", "explanation": "There is no way to partition the nodes into two independent sets such that every edge connects a node in one and a node in the other."},
            {"input": "graph = [[1,3],[0,2],[1,3],[0,2]]", "output": "true", "explanation": "We can partition the nodes into two sets: {0, 2} and {1, 3}."}
        ],
        "constraints": [
            "graph.length == n",
            "1 <= n <= 100",
            "0 <= graph[u].length < n",
            "0 <= graph[u][i] <= n - 1",
            "graph[u] does not contain u.",
            "All the values of graph[u] are unique.",
            "If graph[u] contains v, then graph[v] contains u."
        ],
        "test_cases": [
            {"input": {"graph": [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]}, "expected": False},
            {"input": {"graph": [[1, 3], [0, 2], [1, 3], [0, 2]]}, "expected": True},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def isBipartite(self, graph: List[List[int]]) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean isBipartite(int[][] graph) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isBipartite(vector<vector<int>>& graph) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    743: {
        "description": "You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.\n\nWe will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.",
        "examples": [
            {"input": "times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2", "output": "2"},
            {"input": "times = [[1,2,1]], n = 2, k = 1", "output": "1"},
            {"input": "times = [[1,2,1]], n = 2, k = 2", "output": "-1"}
        ],
        "constraints": [
            "1 <= k <= n <= 100",
            "1 <= times.length <= 6000",
            "times[i].length == 3",
            "1 <= ui, vi <= n",
            "ui != vi",
            "0 <= wi <= 100",
            "All the pairs (ui, vi) are unique."
        ],
        "test_cases": [
            {"input": {"times": [[2, 1, 1], [2, 3, 1], [3, 4, 1]], "n": 4, "k": 2}, "expected": 2},
            {"input": {"times": [[1, 2, 1]], "n": 2, "k": 1}, "expected": 1},
            {"input": {"times": [[1, 2, 1]], "n": 2, "k": 2}, "expected": -1},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int networkDelayTime(int[][] times, int n, int k) {\n        // Write your solution here\n        return -1;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int networkDelayTime(vector<vector<int>>& times, int n, int k) {\n        // Write your solution here\n        return -1;\n    }\n};\n"
        }
    },
    70: {
        "description": "You are climbing a staircase. It takes n steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "There are two ways to climb to the top.\n1. 1 step + 1 step\n2. 2 steps"},
            {"input": "n = 3", "output": "3", "explanation": "There are three ways to climb to the top.\n1. 1 step + 1 step + 1 step\n2. 1 step + 2 steps\n3. 2 steps + 1 step"}
        ],
        "constraints": [
            "1 <= n <= 45"
        ],
        "test_cases": [
            {"input": {"n": 2}, "expected": 2},
            {"input": {"n": 3}, "expected": 3},
            {"input": {"n": 5}, "expected": 8},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int climbStairs(int n) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int climbStairs(int n) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    322: {
        "description": "You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.\n\nReturn the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.\n\nYou may assume that you have an infinite number of each kind of coin.",
        "examples": [
            {"input": "coins = [1,2,5], amount = 11", "output": "3", "explanation": "11 = 5 + 5 + 1"},
            {"input": "coins = [2], amount = 3", "output": "-1"},
            {"input": "coins = [1], amount = 0", "output": "0"}
        ],
        "constraints": [
            "1 <= coins.length <= 12",
            "1 <= coins[i] <= 2^31 - 1",
            "0 <= amount <= 10^4"
        ],
        "test_cases": [
            {"input": {"coins": [1, 2, 5], "amount": 11}, "expected": 3},
            {"input": {"coins": [2], "amount": 3}, "expected": -1},
            {"input": {"coins": [1], "amount": 0}, "expected": 0},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def coinChange(self, coins: List[int], amount: int) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int coinChange(int[] coins, int amount) {\n        // Write your solution here\n        return -1;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int coinChange(vector<int>& coins, int amount) {\n        // Write your solution here\n        return -1;\n    }\n};\n"
        }
    },
    198: {
        "description": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.\n\nGiven an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Rob house 1 (money = 1) and then rob house 3 (money = 3). Total amount you can rob = 1 + 3 = 4."},
            {"input": "nums = [2,7,9,3,1]", "output": "12", "explanation": "Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1). Total amount you can rob = 2 + 9 + 1 = 12."}
        ],
        "constraints": [
            "1 <= nums.length <= 100",
            "0 <= nums[i] <= 400"
        ],
        "test_cases": [
            {"input": {"nums": [1, 2, 3, 1]}, "expected": 4},
            {"input": {"nums": [2, 7, 9, 3, 1]}, "expected": 12},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def rob(self, nums: List[int]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int rob(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int rob(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    300: {
        "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence.\n\nA subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.",
        "examples": [
            {"input": "nums = [10,9,2,5,3,7,101,18]", "output": "4", "explanation": "The longest increasing subsequence is [2,3,7,101], therefore the length is 4."},
            {"input": "nums = [0,1,0,3,2,3]", "output": "4"},
            {"input": "nums = [7,7,7,7,7,7,7]", "output": "1"}
        ],
        "constraints": [
            "1 <= nums.length <= 2500",
            "-10^4 <= nums[i] <= 10^4"
        ],
        "test_cases": [
            {"input": {"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, "expected": 4},
            {"input": {"nums": [0, 1, 0, 3, 2, 3]}, "expected": 4},
            {"input": {"nums": [7, 7, 7, 7, 7, 7, 7]}, "expected": 1},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def lengthOfLIS(self, nums: List[int]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int lengthOfLIS(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int lengthOfLIS(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    1143: {
        "description": "Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.\n\nA subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.\n\nA common subsequence of two strings is a subsequence that is common to both strings.",
        "examples": [
            {"input": "text1 = \"abcde\", text2 = \"ace\"", "output": "3", "explanation": "The longest common subsequence is \"ace\" and its length is 3."},
            {"input": "text1 = \"abc\", text2 = \"abc\"", "output": "3", "explanation": "The longest common subsequence is \"abc\" and its length is 3."},
            {"input": "text1 = \"abc\", text2 = \"def\"", "output": "0", "explanation": "There is no such common subsequence, so the result is 0."}
        ],
        "constraints": [
            "1 <= text1.length, text2.length <= 1000",
            "text1 and text2 consist of only lowercase English characters."
        ],
        "test_cases": [
            {"input": {"text1": "abcde", "text2": "ace"}, "expected": 3},
            {"input": {"text1": "abc", "text2": "abc"}, "expected": 3},
            {"input": {"text1": "abc", "text2": "def"}, "expected": 0},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def longestCommonSubsequence(self, text1: str, text2: str) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int longestCommonSubsequence(String text1, String text2) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int longestCommonSubsequence(string text1, string text2) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    416: {
        "description": "Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.",
        "examples": [
            {"input": "nums = [1,5,11,5]", "output": "true", "explanation": "The array can be partitioned as [1, 5, 5] and [11]."},
            {"input": "nums = [1,2,3,5]", "output": "false", "explanation": "The array cannot be partitioned into equal sum subsets."}
        ],
        "constraints": [
            "1 <= nums.length <= 200",
            "1 <= nums[i] <= 100"
        ],
        "test_cases": [
            {"input": {"nums": [1, 5, 11, 5]}, "expected": True},
            {"input": {"nums": [1, 2, 3, 5]}, "expected": False},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def canPartition(self, nums: List[int]) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean canPartition(int[] nums) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool canPartition(vector<int>& nums) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    72: {
        "description": "Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.\n\nYou have the following three operations permitted on a word:\n- Insert a character\n- Delete a character\n- Replace a character",
        "examples": [
            {"input": "word1 = \"horse\", word2 = \"ros\"", "output": "3", "explanation": "horse -> rorse (replace 'h' with 'r')\nrorse -> rose (remove 'r')\nrose -> ros (remove 'e')"},
            {"input": "word1 = \"intention\", word2 = \"execution\"", "output": "5", "explanation": "intention -> inention (remove 't')\ninention -> enention (replace 'i' with 'e')\nenention -> exention (replace 'n' with 'x')\nexention -> exection (replace 'n' with 'c')\nexection -> execution (insert 'u')"}
        ],
        "constraints": [
            "0 <= word1.length, word2.length <= 500",
            "word1 and word2 consist of lowercase English letters."
        ],
        "test_cases": [
            {"input": {"word1": "horse", "word2": "ros"}, "expected": 3},
            {"input": {"word1": "intention", "word2": "execution"}, "expected": 5},
            {"input": {"word1": "", "word2": ""}, "expected": 0},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def minDistance(self, word1: str, word2: str) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int minDistance(String word1, String word2) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int minDistance(string word1, string word2) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    46: {
        "description": "Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.",
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"},
            {"input": "nums = [0,1]", "output": "[[0,1],[1,0]]"},
            {"input": "nums = [1]", "output": "[[1]]"}
        ],
        "constraints": [
            "1 <= nums.length <= 6",
            "-10 <= nums[i] <= 10",
            "All the integers of nums are unique."
        ],
        "test_cases": [
            {"input": {"nums": [1, 2, 3]}, "expected": [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]},
            {"input": {"nums": [0, 1]}, "expected": [[0, 1], [1, 0]]},
            {"input": {"nums": [1]}, "expected": [[1]]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def permute(self, nums: List[int]) -> List[List[int]]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> permute(int[] nums) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> permute(vector<int>& nums) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        }
    }
}
