CHUNK_4 = {
    33: {
        "description": "There is an integer array nums sorted in ascending order (with distinct values).\n\nPrior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed).\n\nGiven the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.\n\nYou must write an algorithm with O(log n) runtime complexity.",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1"},
            {"input": "nums = [1], target = 0", "output": "-1"}
        ],
        "constraints": [
            "1 <= nums.length <= 5000",
            "-10^4 <= nums[i] <= 10^4",
            "All values of nums are unique.",
            "nums is an ascending array that is possibly rotated.",
            "-10^4 <= target <= 10^4"
        ],
        "test_cases": [
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 0}, "expected": 4},
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2], "target": 3}, "expected": -1},
            {"input": {"nums": [1], "target": 0}, "expected": -1},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int search(int[] nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n};\n"
        }
    },
    153: {
        "description": "Suppose an array of length n sorted in ascending order is rotated between 1 and n times.\n\nGiven the sorted rotated array nums of unique elements, return the minimum element of this array.\n\nYou must write an algorithm that runs in O(log n) time.",
        "examples": [
            {"input": "nums = [3,4,5,1,2]", "output": "1", "explanation": "The original array was [1,2,3,4,5] rotated 3 times."},
            {"input": "nums = [4,5,6,7,0,1,2]", "output": "0", "explanation": "The original array was [0,1,2,4,5,6,7] and it was rotated 4 times."},
            {"input": "nums = [11,13,15,17]", "output": "11"}
        ],
        "constraints": [
            "n == nums.length",
            "1 <= n <= 5000",
            "-5000 <= nums[i] <= 5000",
            "All the integers of nums are unique.",
            "nums is sorted and rotated between 1 and n times."
        ],
        "test_cases": [
            {"input": {"nums": [3, 4, 5, 1, 2]}, "expected": 1},
            {"input": {"nums": [4, 5, 6, 7, 0, 1, 2]}, "expected": 0},
            {"input": {"nums": [11, 13, 15, 17]}, "expected": 11},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def findMin(self, nums: List[int]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int findMin(int[] nums) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int findMin(vector<int>& nums) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    74: {
        "description": "You are given an m x n integer matrix matrix with the following two properties:\n- Each row is sorted in non-decreasing order.\n- The first integer of each row is greater than the last integer of the previous row.\n\nGiven an integer target, return true if target is in matrix or false otherwise.\n\nYou must write a solution in O(log(m * n)) time complexity.",
        "examples": [
            {"input": "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3", "output": "true"},
            {"input": "matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13", "output": "false"}
        ],
        "constraints": [
            "m == matrix.length",
            "n == matrix[i].length",
            "1 <= m, n <= 100",
            "-10^4 <= matrix[i][j], target <= 10^4"
        ],
        "test_cases": [
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 3}, "expected": True},
            {"input": {"matrix": [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], "target": 13}, "expected": False},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean searchMatrix(int[][] matrix, int target) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool searchMatrix(vector<vector<int>>& matrix, int target) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    34: {
        "description": "Given an array of integers nums sorted in non-decreasing order, find the starting and ending position of a given target value.\n\nIf target is not found in the array, return [-1, -1].\n\nYou must write an algorithm with O(log n) runtime complexity.",
        "examples": [
            {"input": "nums = [5,7,7,8,8,10], target = 8", "output": "[3,4]"},
            {"input": "nums = [5,7,7,8,8,10], target = 6", "output": "[-1,-1]"},
            {"input": "nums = [], target = 0", "output": "[-1,-1]"}
        ],
        "constraints": [
            "0 <= nums.length <= 10^5",
            "-10^9 <= nums[i] <= 10^9",
            "nums is a non-decreasing array.",
            "-10^9 <= target <= 10^9"
        ],
        "test_cases": [
            {"input": {"nums": [5, 7, 7, 8, 8, 10], "target": 8}, "expected": [3, 4]},
            {"input": {"nums": [5, 7, 7, 8, 8, 10], "target": 6}, "expected": [-1, -1]},
            {"input": {"nums": [], "target": 0}, "expected": [-1, -1]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def searchRange(self, nums: List[int], target: int) -> List[int]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int[] searchRange(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{-1, -1};\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> searchRange(vector<int>& nums, int target) {\n        // Write your solution here\n        return {-1, -1};\n    }\n};\n"
        }
    },
    215: {
        "description": "Given an integer array nums and an integer k, return the kth largest element in the array.\n\nNote that it is the kth largest element in the sorted order, not the kth distinct element.\n\nCan you solve it without sorting?",
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5"},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4"}
        ],
        "constraints": [
            "1 <= k <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4"
        ],
        "test_cases": [
            {"input": {"nums": [3, 2, 1, 5, 6, 4], "k": 2}, "expected": 5},
            {"input": {"nums": [3, 2, 3, 1, 2, 4, 5, 5, 6], "k": 4}, "expected": 4},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def findKthLargest(self, nums: List[int], k: int) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int findKthLargest(int[] nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int findKthLargest(vector<int>& nums, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    226: {
        "description": "Given the root of a binary tree, invert the tree, and return its root.",
        "examples": [
            {"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]"},
            {"input": "root = [2,1,3]", "output": "[2,3,1]"},
            {"input": "root = []", "output": "[]"}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [0, 100].",
            "-100 <= Node.val <= 100"
        ],
        "test_cases": [
            {"input": {"root": [4, 2, 7, 1, 3, 6, 9]}, "expected": [4, 7, 2, 9, 6, 3, 1]},
            {"input": {"root": [2, 1, 3]}, "expected": [2, 3, 1]},
            {"input": {"root": []}, "expected": []},
        ],
        "starter_codes": {
            "python": "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\n/**\n * Definition for a binary tree node.\n * public class TreeNode {\n *     int val;\n *     TreeNode left;\n *     TreeNode right;\n *     TreeNode() {}\n *     TreeNode(int val) { this.val = val; }\n *     TreeNode(int val, TreeNode left, TreeNode right) {\n *         this.val = val;\n *         this.left = left;\n *         this.right = right;\n *     }\n * }\n */\nclass Solution {\n    public TreeNode invertTree(TreeNode root) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\n/**\n * Definition for a binary tree node.\n * struct TreeNode {\n *     int val;\n *     TreeNode *left;\n *     TreeNode *right;\n *     TreeNode() : val(0), left(nullptr), right(nullptr) {}\n *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}\n * };\n */\nclass Solution {\npublic:\n    TreeNode* invertTree(TreeNode* root) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    104: {
        "description": "Given the root of a binary tree, return its maximum depth.\n\nA binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3"},
            {"input": "root = [1,null,2]", "output": "2"}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [0, 10^4].",
            "-100 <= Node.val <= 100"
        ],
        "test_cases": [
            {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "expected": 3},
            {"input": {"root": [1, None, 2]}, "expected": 2},
        ],
        "starter_codes": {
            "python": "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\nclass Solution:\n    def maxDepth(self, root: Optional[TreeNode]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int maxDepth(TreeNode root) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxDepth(TreeNode* root) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    543: {
        "description": "Given the root of a binary tree, return the length of the diameter of the tree.\n\nThe diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.\n\nThe length of a path between two nodes is represented by the number of edges between them.",
        "examples": [
            {"input": "root = [1,2,3,4,5]", "output": "3", "explanation": "3 is the length of the path [4,2,1,3] or [5,2,1,3]."},
            {"input": "root = [1,2]", "output": "1"}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [1, 10^4].",
            "-100 <= Node.val <= 100"
        ],
        "test_cases": [
            {"input": {"root": [1, 2, 3, 4, 5]}, "expected": 3},
            {"input": {"root": [1, 2]}, "expected": 1},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int diameterOfBinaryTree(TreeNode root) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int diameterOfBinaryTree(TreeNode* root) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    102: {
        "description": "Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"},
            {"input": "root = [1]", "output": "[[1]]"},
            {"input": "root = []", "output": "[]"}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [0, 2000].",
            "-1000 <= Node.val <= 1000"
        ],
        "test_cases": [
            {"input": {"root": [3, 9, 20, None, None, 15, 7]}, "expected": [[3], [9, 20], [15, 7]]},
            {"input": {"root": [1]}, "expected": [[1]]},
            {"input": {"root": []}, "expected": []},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public List<List<Integer>> levelOrder(TreeNode root) {\n        // Write your solution here\n        return new ArrayList<>();\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<vector<int>> levelOrder(TreeNode* root) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        }
    },
    98: {
        "description": "Given the root of a binary tree, determine if it is a valid binary search tree (BST).\n\nA valid BST is defined as follows:\n- The left subtree of a node contains only nodes with keys less than the node's key.\n- The right subtree of a node contains only nodes with keys greater than the node's key.\n- Both the left and right subtrees must also be binary search trees.",
        "examples": [
            {"input": "root = [2,1,3]", "output": "true"},
            {"input": "root = [5,1,4,null,null,3,6]", "output": "false", "explanation": "The root node's value is 5 but its right child's value is 4."}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [1, 10^4].",
            "-2^31 <= Node.val <= 2^31 - 1"
        ],
        "test_cases": [
            {"input": {"root": [2, 1, 3]}, "expected": True},
            {"input": {"root": [5, 1, 4, None, None, 3, 6]}, "expected": False},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def isValidBST(self, root: Optional[TreeNode]) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public boolean isValidBST(TreeNode root) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool isValidBST(TreeNode* root) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    235: {
        "description": "Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.\n\nAccording to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”",
        "examples": [
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "output": "6", "explanation": "The LCA of nodes 2 and 8 is 6."},
            {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4", "output": "2", "explanation": "The LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself according to the LCA definition."}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [2, 10^5].",
            "-10^9 <= Node.val <= 10^9",
            "All Node.val are unique.",
            "p != q",
            "p and q will exist in the BST."
        ],
        "test_cases": [
            {"input": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 8}, "expected": 6},
            {"input": {"root": [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], "p": 2, "q": 4}, "expected": 2},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    236: {
        "description": "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.\n\nAccording to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”",
        "examples": [
            {"input": "root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1", "output": "3", "explanation": "The LCA of nodes 5 and 1 is 3."},
            {"input": "root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4", "output": "5", "explanation": "The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition."}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [2, 10^5].",
            "-10^9 <= Node.val <= 10^9",
            "All Node.val are unique.",
            "p != q",
            "p and q will exist in the tree."
        ],
        "test_cases": [
            {"input": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 5, "q": 1}, "expected": 3},
            {"input": {"root": [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], "p": 5, "q": 4}, "expected": 5},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    105: {
        "description": "Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.",
        "examples": [
            {"input": "preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "output": "[3,9,20,null,null,15,7]"},
            {"input": "preorder = [-1], inorder = [-1]", "output": "[-1]"}
        ],
        "constraints": [
            "1 <= preorder.length <= 3000",
            "inorder.length == preorder.length",
            "-3000 <= preorder[i], inorder[i] <= 3000",
            "preorder and inorder consist of unique values.",
            "Each value of inorder also appears in preorder.",
            "preorder is guaranteed to be the preorder traversal of the tree.",
            "inorder is guaranteed to be the inorder traversal of the tree."
        ],
        "test_cases": [
            {"input": {"preorder": [3, 9, 20, 15, 7], "inorder": [9, 3, 15, 20, 7]}, "expected": [3, 9, 20, None, None, 15, 7]},
            {"input": {"preorder": [-1], "inorder": [-1]}, "expected": [-1]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public TreeNode buildTree(int[] preorder, int[] inorder) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    124: {
        "description": "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.\n\nThe path sum of a path is the sum of the node's values in the path.\n\nGiven the root of a binary tree, return the maximum path sum of any non-empty path.",
        "examples": [
            {"input": "root = [1,2,3]", "output": "6", "explanation": "The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6."},
            {"input": "root = [-10,9,20,null,null,15,7]", "output": "42", "explanation": "The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42."}
        ],
        "constraints": [
            "The number of nodes in the tree is in the range [1, 3 * 10^4].",
            "-1000 <= Node.val <= 1000"
        ],
        "test_cases": [
            {"input": {"root": [1, 2, 3]}, "expected": 6},
            {"input": {"root": [-10, 9, 20, None, None, 15, 7]}, "expected": 42},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def maxPathSum(self, root: Optional[TreeNode]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int maxPathSum(TreeNode root) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int maxPathSum(TreeNode* root) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    200: {
        "description": "Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.\n\nAn island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.",
        "examples": [
            {"input": "grid = [\n  [\"1\",\"1\",\"1\",\"1\",\"0\"],\n  [\"1\",\"1\",\"0\",\"1\",\"0\"],\n  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n  [\"0\",\"0\",\"0\",\"0\",\"0\"]\n]", "output": "1"},
            {"input": "grid = [\n  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n  [\"0\",\"0\",\"1\",\"0\",\"0\"],\n  [\"0\",\"0\",\"0\",\"1\",\"1\"]\n]", "output": "3"}
        ],
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 <= m, n <= 300",
            "grid[i][j] is '0' or '1'."
        ],
        "test_cases": [
            {"input": {"grid": [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]}, "expected": 1},
            {"input": {"grid": [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]}, "expected": 3},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def numIslands(self, grid: List[List[str]]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int numIslands(char[][] grid) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int numIslands(vector<vector<char>>& grid) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    }
}
