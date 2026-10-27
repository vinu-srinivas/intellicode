CHUNK_3 = {
    206: {
        "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"},
            {"input": "head = [1,2]", "output": "[2,1]"},
            {"input": "head = []", "output": "[]"}
        ],
        "constraints": [
            "The number of nodes in the list is the range [0, 5000].",
            "-5000 <= Node.val <= 5000"
        ],
        "test_cases": [
            {"input": {"head": [1, 2, 3, 4, 5]}, "expected": [5, 4, 3, 2, 1]},
            {"input": {"head": [1, 2]}, "expected": [2, 1]},
            {"input": {"head": []}, "expected": []},
        ],
        "starter_codes": {
            "python": "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\n/**\n * Definition for singly-linked list.\n * public class ListNode {\n *     int val;\n *     ListNode next;\n *     ListNode() {}\n *     ListNode(int val) { this.val = val; }\n *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }\n * }\n */\nclass Solution {\n    public ListNode reverseList(ListNode head) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\n/**\n * Definition for singly-linked list.\n * struct ListNode {\n *     int val;\n *     ListNode *next;\n *     ListNode() : val(0), next(nullptr) {}\n *     ListNode(int x) : val(x), next(nullptr) {}\n *     ListNode(int x, ListNode *next) : val(x), next(next) {}\n * };\n */\nclass Solution {\npublic:\n    ListNode* reverseList(ListNode* head) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    21: {
        "description": "You are given the heads of two sorted linked lists list1 and list2.\n\nMerge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.\n\nReturn the head of the merged linked list.",
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]"},
            {"input": "list1 = [], list2 = []", "output": "[]"},
            {"input": "list1 = [], list2 = [0]", "output": "[0]"}
        ],
        "constraints": [
            "The number of nodes in both lists is in the range [0, 50].",
            "-100 <= Node.val <= 100",
            "Both list1 and list2 are sorted in non-decreasing order."
        ],
        "test_cases": [
            {"input": {"list1": [1, 2, 4], "list2": [1, 3, 4]}, "expected": [1, 1, 2, 3, 4, 4]},
            {"input": {"list1": [], "list2": []}, "expected": []},
        ],
        "starter_codes": {
            "python": "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\nclass Solution:\n    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    141: {
        "description": "Given head, the head of a linked list, determine if the linked list has a cycle in it.\n\nThere is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.\n\nReturn true if there is a cycle in the linked list. Otherwise, return false.",
        "examples": [
            {"input": "head = [3,2,0,-4], pos = 1", "output": "true", "explanation": "There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed)."},
            {"input": "head = [1,2], pos = 0", "output": "true", "explanation": "There is a cycle in the linked list, where the tail connects to the 0th node."},
            {"input": "head = [1], pos = -1", "output": "false", "explanation": "There is no cycle in the linked list."}
        ],
        "constraints": [
            "The number of the nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "pos is -1 or a valid index in the linked-list."
        ],
        "test_cases": [
            {"input": {"head": [3, 2, 0, -4]}, "expected": True},
            {"input": {"head": [1]}, "expected": False},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def hasCycle(self, head: Optional[ListNode]) -> bool:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\npublic class Solution {\n    public boolean hasCycle(ListNode head) {\n        // Write your solution here\n        return false;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    bool hasCycle(ListNode *head) {\n        // Write your solution here\n        return false;\n    }\n};\n"
        }
    },
    19: {
        "description": "Given the head of a linked list, remove the nth node from the end of the list and return its head.",
        "examples": [
            {"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]"},
            {"input": "head = [1], n = 1", "output": "[]"},
            {"input": "head = [1,2], n = 1", "output": "[1]"}
        ],
        "constraints": [
            "The number of nodes in the list is sz.",
            "1 <= sz <= 30",
            "0 <= Node.val <= 100",
            "1 <= n <= sz"
        ],
        "test_cases": [
            {"input": {"head": [1, 2, 3, 4, 5], "n": 2}, "expected": [1, 2, 3, 5]},
            {"input": {"head": [1], "n": 1}, "expected": []},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public ListNode removeNthFromEnd(ListNode head, int n) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    ListNode* removeNthFromEnd(ListNode* head, int n) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    160: {
        "description": "Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null.",
        "examples": [
            {"input": "intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3", "output": "Intersected at '8'"},
            {"input": "intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2", "output": "No intersection"}
        ],
        "constraints": [
            "The number of nodes of listA is in the m.",
            "The number of nodes of listB is in the n.",
            "1 <= m, n <= 3 * 10^4",
            "1 <= Node.val <= 10^5"
        ],
        "test_cases": [
            {"input": {"listA": [4, 1, 8, 4, 5], "listB": [5, 6, 1, 8, 4, 5]}, "expected": 8},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\npublic class Solution {\n    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    2: {
        "description": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\n\nYou may assume the two numbers do not contain any leading zero, except the number 0 itself.",
        "examples": [
            {"input": "l1 = [2,4,3], l2 = [5,6,4]", "output": "[7,0,8]", "explanation": "342 + 465 = 807."},
            {"input": "l1 = [0], l2 = [0]", "output": "[0]"},
            {"input": "l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]", "output": "[8,9,9,9,0,0,0,1]"}
        ],
        "constraints": [
            "The number of nodes in each linked list is in the range [1, 100].",
            "0 <= Node.val <= 9",
            "It is guaranteed that the list represents a number that does not have leading zeros."
        ],
        "test_cases": [
            {"input": {"l1": [2, 4, 3], "l2": [5, 6, 4]}, "expected": [7, 0, 8]},
            {"input": {"l1": [0], "l2": [0]}, "expected": [0]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    138: {
        "description": "A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null.\n\nConstruct a deep copy of the list. The deep copy should consist of exactly n brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the next and random pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state.\n\nReturn the head of the copied linked list.",
        "examples": [
            {"input": "head = [[7,null],[13,0],[11,4],[10,2],[1,0]]", "output": "[[7,null],[13,0],[11,4],[10,2],[1,0]]"},
            {"input": "head = [[1,1],[2,1]]", "output": "[[1,1],[2,1]]"}
        ],
        "constraints": [
            "0 <= n <= 1000",
            "-10^4 <= Node.val <= 10^4",
            "Node.random is null or is pointing to some node in the linked list."
        ],
        "test_cases": [
            {"input": {"head": [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]}, "expected": [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public Node copyRandomList(Node head) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    Node* copyRandomList(Node* head) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    23: {
        "description": "You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.\n\nMerge all the linked-lists into one sorted linked-list and return it.",
        "examples": [
            {"input": "lists = [[1,4,5],[1,3,4],[2,6]]", "output": "[1,1,2,3,4,4,5,6]", "explanation": "The linked-lists are:\n[\n  1->4->5,\n  1->3->4,\n  2->6\n]\nmerging them into one sorted list:\n1->1->2->3->4->4->5->6"},
            {"input": "lists = []", "output": "[]"},
            {"input": "lists = [[]]", "output": "[]"}
        ],
        "constraints": [
            "k == lists.length",
            "0 <= k <= 10^4",
            "0 <= lists[i].length <= 500",
            "-10^4 <= lists[i][j] <= 10^4",
            "lists[i] is sorted in ascending order.",
            "The sum of lists[i].length will not exceed 10^4."
        ],
        "test_cases": [
            {"input": {"lists": [[1, 4, 5], [1, 3, 4], [2, 6]]}, "expected": [1, 1, 2, 3, 4, 4, 5, 6]},
            {"input": {"lists": []}, "expected": []},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public ListNode mergeKLists(ListNode[] lists) {\n        // Write your solution here\n        return null;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    ListNode* mergeKLists(vector<ListNode*>& lists) {\n        // Write your solution here\n        return nullptr;\n    }\n};\n"
        }
    },
    155: {
        "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.\n\nImplement the MinStack class:\n- MinStack() initializes the stack object.\n- void push(int val) pushes the element val onto the stack.\n- void pop() removes the element on the top of the stack.\n- int top() gets the top element of the stack.\n- int getMin() retrieves the minimum element in the stack.\n\nYou must implement a solution with O(1) time complexity for each function.",
        "examples": [
            {"input": "[\"MinStack\",\"push\",\"push\",\"push\",\"getMin\",\"pop\",\"top\",\"getMin\"]\n[[],[-2],[0],[-3],[],[],[],[]]", "output": "[null,null,null,null,-3,null,0,-2]"}
        ],
        "constraints": [
            "-2^31 <= val <= 2^31 - 1",
            "Methods pop, top and getMin operations will always be called on non-empty stacks.",
            "At most 3 * 10^4 calls will be made to push, pop, top, and getMin."
        ],
        "test_cases": [
            {"input": {"operations": ["push", "push", "getMin"], "values": [-2, 0, None]}, "expected": -2},
        ],
        "starter_codes": {
            "python": "class MinStack:\n\n    def __init__(self):\n        # Write your solution here\n        pass\n\n    def push(self, val: int) -> None:\n        pass\n\n    def pop(self) -> None:\n        pass\n\n    def top(self) -> int:\n        return 0\n\n    def getMin(self) -> int:\n        return 0\n",
            "java": "import java.util.*;\n\nclass MinStack {\n\n    public MinStack() {\n        // Write your solution here\n    }\n\n    public void push(int val) {\n    }\n\n    public void pop() {\n    }\n\n    public int top() {\n        return 0;\n    }\n\n    public int getMin() {\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass MinStack {\npublic:\n    MinStack() {\n        // Write your solution here\n    }\n\n    void push(int val) {\n    }\n\n    void pop() {\n    }\n\n    int top() {\n        return 0;\n    }\n\n    int getMin() {\n        return 0;\n    }\n};\n"
        }
    },
    739: {
        "description": "Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.",
        "examples": [
            {"input": "temperatures = [73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]"},
            {"input": "temperatures = [30,40,50,60]", "output": "[1,1,1,0]"},
            {"input": "temperatures = [30,60,90]", "output": "[1,1,0]"}
        ],
        "constraints": [
            "1 <= temperatures.length <= 10^5",
            "30 <= temperatures[i] <= 100"
        ],
        "test_cases": [
            {"input": {"temperatures": [73, 74, 75, 71, 69, 72, 76, 73]}, "expected": [1, 1, 4, 2, 1, 1, 0, 0]},
            {"input": {"temperatures": [30, 40, 50, 60]}, "expected": [1, 1, 1, 0]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int[] dailyTemperatures(int[] temperatures) {\n        // Write your solution here\n        return new int[0];\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> dailyTemperatures(vector<int>& temperatures) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        }
    },
    496: {
        "description": "The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.\n\nYou are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.\n\nFor each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.\n\nReturn an array ans of length nums1.length such that ans[i] is the next greater element as described above.",
        "examples": [
            {"input": "nums1 = [4,1,2], nums2 = [1,3,4,2]", "output": "[-1,3,-1]", "explanation": "4 is in nums2 at index 2, no next greater -> -1.\n1 is at index 0, next greater is 3.\n2 is at index 3, no next greater -> -1."},
            {"input": "nums1 = [2,4], nums2 = [1,2,3,4]", "output": "[3,-1]"}
        ],
        "constraints": [
            "1 <= nums1.length <= nums2.length <= 1000",
            "0 <= nums1[i], nums2[i] <= 10^4",
            "All integers in nums1 and nums2 are unique.",
            "All the integers of nums1 also appear in nums2."
        ],
        "test_cases": [
            {"input": {"nums1": [4, 1, 2], "nums2": [1, 3, 4, 2]}, "expected": [-1, 3, -1]},
            {"input": {"nums1": [2, 4], "nums2": [1, 2, 3, 4]}, "expected": [3, -1]},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int[] nextGreaterElement(int[] nums1, int[] nums2) {\n        // Write your solution here\n        return new int[0];\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        }
    },
    150: {
        "description": "You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.\n\nEvaluate the expression. Return an integer that represents the value of the expression.\n\nNote that:\n- The valid operators are '+', '-', '*', and '/'.\n- Each operand may be an integer or another expression.\n- The division between two integers always truncates toward zero.\n- There will not be any division by zero.\n- The input represents a valid arithmetic expression in a reverse polish notation.",
        "examples": [
            {"input": "tokens = [\"2\",\"1\",\"+\",\"3\",\"*\"]", "output": "9", "explanation": "((2 + 1) * 3) = 9"},
            {"input": "tokens = [\"4\",\"13\",\"5\",\"/\",\"+\"]", "output": "6", "explanation": "(4 + (13 / 5)) = 6"},
            {"input": "tokens = [\"10\",\"6\",\"9\",\"3\",\"+\",\"-11\",\"*\",\"/\",\"*\",\"17\",\"+\",\"5\",\"+\"]", "output": "22"}
        ],
        "constraints": [
            "1 <= tokens.length <= 10^4",
            "tokens[i] is either an operator: \"+\", \"-\", \"*\", or \"/\", or an integer in the range [-200, 200]."
        ],
        "test_cases": [
            {"input": {"tokens": ["2", "1", "+", "3", "*"]}, "expected": 9},
            {"input": {"tokens": ["4", "13", "5", "/", "+"]}, "expected": 6},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def evalRPN(self, tokens: List[str]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int evalRPN(String[] tokens) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int evalRPN(vector<string>& tokens) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    84: {
        "description": "Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.",
        "examples": [
            {"input": "heights = [2,1,5,6,2,3]", "output": "10", "explanation": "The above is a histogram where width of each bar is 1. The largest rectangle is shown in the red area, which has an area = 10 units."},
            {"input": "heights = [2,4]", "output": "4"}
        ],
        "constraints": [
            "1 <= heights.length <= 10^5",
            "0 <= heights[i] <= 10^4"
        ],
        "test_cases": [
            {"input": {"heights": [2, 1, 5, 6, 2, 3]}, "expected": 10},
            {"input": {"heights": [2, 4]}, "expected": 4},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def largestRectangleArea(self, heights: List[int]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int largestRectangleArea(int[] heights) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int largestRectangleArea(vector<int>& heights) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    853: {
        "description": "There are n cars at given miles away from the starting mile 0, traveling to reach the mile target.\n\nYou are given two integer array position and speed, both of length n, where position[i] is the starting position of the ith car and speed[i] is the speed of the ith car in miles per hour.\n\nA car cannot pass another car, but it can catch up and then travel next to it at the speed of the slower car.\n\nA car fleet is a car or cars driving next to each other. The speed of the car fleet is the minimum speed of any car in the fleet.\n\nReturn the number of car fleets that will arrive at the destination.",
        "examples": [
            {"input": "target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]", "output": "3"},
            {"input": "target = 10, position = [3], speed = [3]", "output": "1"},
            {"input": "target = 100, position = [0,2,4], speed = [4,2,1]", "output": "1"}
        ],
        "constraints": [
            "n == position.length == speed.length",
            "1 <= n <= 10^5",
            "0 < target <= 10^6",
            "0 <= position[i] < target",
            "All the values of position are unique.",
            "0 < speed[i] <= 10^6"
        ],
        "test_cases": [
            {"input": {"target": 12, "position": [10, 8, 0, 5, 3], "speed": [2, 4, 1, 1, 3]}, "expected": 3},
            {"input": {"target": 10, "position": [3], "speed": [3]}, "expected": 1},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int carFleet(int target, int[] position, int[] speed) {\n        // Write your solution here\n        return 0;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int carFleet(int target, vector<int>& position, vector<int>& speed) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        }
    },
    704: {
        "description": "Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.\n\nYou must write an algorithm with O(log n) runtime complexity.",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4", "explanation": "9 exists in nums and its index is 4."},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1", "explanation": "2 does not exist in nums so return -1."}
        ],
        "constraints": [
            "1 <= nums.length <= 10^4",
            "-10^4 < nums[i], target < 10^4",
            "All the integers in nums are unique.",
            "nums is sorted in ascending order."
        ],
        "test_cases": [
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 9}, "expected": 4},
            {"input": {"nums": [-1, 0, 3, 5, 9, 12], "target": 2}, "expected": -1},
        ],
        "starter_codes": {
            "python": "class Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        # Write your solution here\n        pass\n",
            "java": "import java.util.*;\n\nclass Solution {\n    public int search(int[] nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n}\n",
            "cpp": "#include <bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n};\n"
        }
    }
}
