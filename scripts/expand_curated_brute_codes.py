# scripts/expand_curated_brute_codes.py
import json

MORE_BRUTES = {
    # 217. Contains Duplicate
    217: {
        "name": "Brute Force (Nested Loops)",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)",
        "explanation": "Compare every pair of elements (i, j) with nested loops and return true if any duplicate is found.",
        "code": {
            "python": """class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] == nums[j]:
                    return True
        return False
""",
            "java": """class Solution {
    public boolean containsDuplicate(int[] nums) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] == nums[j]) {
                    return true;
                }
            }
        }
        return false;
    }
}
""",
            "cpp": """#include <vector>
using namespace std;

class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        for (size_t i = 0; i < nums.size(); i++) {
            for (size_t j = i + 1; j < nums.size(); j++) {
                if (nums[i] == nums[j]) {
                    return true;
                }
            }
        }
        return false;
    }
};
"""
        }
    },

    # 238. Product of Array Except Self
    238: {
        "name": "Brute Force (Nested Product)",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(1)",
        "explanation": "For each index i, multiply all numbers at indices j != i using an inner loop.",
        "code": {
            "python": """class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        ans = [1] * n
        for i in range(n):
            prod = 1
            for j in range(n):
                if i != j:
                    prod *= nums[j]
            ans[i] = prod
        return ans
""",
            "java": """class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] ans = new int[n];
        for (int i = 0; i < n; i++) {
            int prod = 1;
            for (int j = 0; j < n; j++) {
                if (i != j) {
                    prod *= nums[j];
                }
            }
            ans[i] = prod;
        }
        return ans;
    }
}
""",
            "cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> ans(n, 1);
        for (int i = 0; i < n; i++) {
            int prod = 1;
            for (int j = 0; j < n; j++) {
                if (i != j) {
                    prod *= nums[j];
                }
            }
            ans[i] = prod;
        }
        return ans;
    }
};
"""
        }
    },

    # 128. Longest Consecutive Sequence
    128: {
        "name": "Brute Force (Linear Array Search)",
        "time_complexity": "O(n^3)",
        "space_complexity": "O(1)",
        "explanation": "For each number x in nums, iteratively check if x + 1, x + 2... exist in nums by searching the array.",
        "code": {
            "python": """class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        if not nums:
            return 0
        longest = 0
        for num in nums:
            curr = num
            streak = 1
            while (curr + 1) in nums:
                curr += 1
                streak += 1
            if streak > longest:
                longest = streak
        return longest
""",
            "java": """class Solution {
    public int longestConsecutive(int[] nums) {
        if (nums.length == 0) {
            return 0;
        }
        int longest = 0;
        for (int num : nums) {
            int curr = num;
            int streak = 1;
            while (contains(nums, curr + 1)) {
                curr++;
                streak++;
            }
            if (streak > longest) {
                longest = streak;
            }
        }
        return longest;
    }

    private boolean contains(int[] nums, int target) {
        for (int x : nums) {
            if (x == target) {
                return true;
            }
        }
        return false;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        if (nums.empty()) {
            return 0;
        }
        int longest = 0;
        for (int num : nums) {
            int curr = num;
            int streak = 1;
            while (find(nums.begin(), nums.end(), curr + 1) != nums.end()) {
                curr++;
                streak++;
            }
            if (streak > longest) {
                longest = streak;
            }
        }
        return longest;
    }
};
"""
        }
    },

    # 206. Reverse Linked List
    206: {
        "name": "Brute Force (Array Reversal)",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "explanation": "Traverse the linked list and store all node values in a list, then iterate backwards to overwrite node values.",
        "code": {
            "python": """class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        values = []
        curr = head
        while curr:
            values.append(curr.val)
            curr = curr.next
        curr = head
        for val in reversed(values):
            curr.val = val
            curr = curr.next
        return head
""",
            "java": """import java.util.*;

class Solution {
    public ListNode reverseList(ListNode head) {
        List<Integer> values = new ArrayList<>();
        ListNode curr = head;
        while (curr != null) {
            values.add(curr.val);
            curr = curr.next;
        }
        curr = head;
        for (int i = values.size() - 1; i >= 0; i--) {
            curr.val = values.get(i);
            curr = curr.next;
        }
        return head;
    }
}
""",
            "cpp": """#include <vector>
using namespace std;

class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        vector<int> values;
        ListNode* curr = head;
        while (curr != nullptr) {
            values.push_back(curr->val);
            curr = curr->next;
        }
        curr = head;
        for (int i = (int)values.size() - 1; i >= 0; i--) {
            curr->val = values[i];
            curr = curr->next;
        }
        return head;
    }
};
"""
        }
    },

    # 21. Merge Two Sorted Lists
    21: {
        "name": "Brute Force (Array Collection & Sort)",
        "time_complexity": "O((n + m) log(n + m))",
        "space_complexity": "O(n + m)",
        "explanation": "Collect all node values from both lists into an array, sort the array, and reconstruct a new linked list.",
        "code": {
            "python": """class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        values = []
        c = list1
        while c:
            values.append(c.val)
            c = c.next
        c = list2
        while c:
            values.append(c.val)
            c = c.next
        values.sort()
        dummy = ListNode(0)
        tail = dummy
        for v in values:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
""",
            "java": """import java.util.*;

class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        List<Integer> values = new ArrayList<>();
        ListNode c = list1;
        while (c != null) {
            values.add(c.val);
            c = c.next;
        }
        c = list2;
        while (c != null) {
            values.add(c.val);
            c = c.next;
        }
        Collections.sort(values);
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        for (int v : values) {
            tail.next = new ListNode(v);
            tail = tail.next;
        }
        return dummy.next;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        vector<int> values;
        ListNode* c = list1;
        while (c != nullptr) {
            values.push_back(c->val);
            c = c->next;
        }
        c = list2;
        while (c != nullptr) {
            values.push_back(c->val);
            c = c->next;
        }
        sort(values.begin(), values.end());
        ListNode dummy(0);
        ListNode* tail = &dummy;
        for (int v : values) {
            tail->next = new ListNode(v);
            tail = tail->next;
        }
        return dummy.next;
    }
};
"""
        }
    },

    # 160. Intersection of Two Linked Lists
    160: {
        "name": "Brute Force (Nested Loop Comparison)",
        "time_complexity": "O(n * m)",
        "space_complexity": "O(1)",
        "explanation": "For every node in list A, traverse the entire list B to check if any node address matches.",
        "code": {
            "python": """class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        currA = headA
        while currA:
            currB = headB
            while currB:
                if currA is currB:
                    return currA
                currB = currB.next
            currA = currA.next
        return None
""",
            "java": """class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode currA = headA;
        while (currA != null) {
            ListNode currB = headB;
            while (currB != null) {
                if (currA == currB) {
                    return currA;
                }
                currB = currB.next;
            }
            currA = currA.next;
        }
        return null;
    }
}
""",
            "cpp": """class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        ListNode* currA = headA;
        while (currA != nullptr) {
            ListNode* currB = headB;
            while (currB != nullptr) {
                if (currA == currB) {
                    return currA;
                }
                currB = currB.next;
            }
            currA = currA.next;
        }
        return nullptr;
    }
};
"""
        }
    },

    # 2. Add Two Numbers
    2: {
        "name": "Brute Force (Digit-by-Digit Simulation)",
        "time_complexity": "O(max(n, m))",
        "space_complexity": "O(max(n, m))",
        "explanation": "Simulate elementary math addition column by column, maintaining a running carry.",
        "code": {
            "python": """class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        curr = dummy
        carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            total = v1 + v2 + carry
            carry = total // 10
            curr.next = ListNode(total % 10)
            curr = curr.next
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
        return dummy.next
""",
            "java": """class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;
        int carry = 0;
        while (l1 != null || l2 != null || carry != 0) {
            int v1 = (l1 != null) ? l1.val : 0;
            int v2 = (l2 != null) ? l2.val : 0;
            int total = v1 + v2 + carry;
            carry = total / 10;
            curr.next = new ListNode(total % 10);
            curr = curr.next;
            if (l1 != null) {
                l1 = l1.next;
            }
            if (l2 != null) {
                l2 = l2.next;
            }
        }
        return dummy.next;
    }
}
""",
            "cpp": """class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode dummy(0);
        ListNode* curr = &dummy;
        int carry = 0;
        while (l1 != nullptr || l2 != nullptr || carry != 0) {
            int v1 = (l1 != nullptr) ? l1->val : 0;
            int v2 = (l2 != nullptr) ? l2->val : 0;
            int total = v1 + v2 + carry;
            carry = total / 10;
            curr->next = new ListNode(total % 10);
            curr = curr->next;
            if (l1 != nullptr) {
                l1 = l1->next;
            }
            if (l2 != nullptr) {
                l2 = l2->next;
            }
        }
        return dummy.next;
    }
};
"""
        }
    },

    # 138. Copy List with Random Pointer
    138: {
        "name": "Brute Force (Two-Pass Pointer Matching)",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(n)",
        "explanation": "Create an unlinked copy of all nodes in pass 1. In pass 2, for each node's random pointer, linearly search the original list to determine the target index, then link the corresponding copy node.",
        "code": {
            "python": """class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return None
        nodes = {}
        curr = head
        while curr:
            nodes[curr] = Node(curr.val)
            curr = curr.next
        curr = head
        while curr:
            if curr.next:
                nodes[curr].next = nodes[curr.next]
            if curr.random:
                nodes[curr].random = nodes[curr.random]
            curr = curr.next
        return nodes[head]
""",
            "java": """import java.util.HashMap;
import java.util.Map;

class Solution {
    public Node copyRandomList(Node head) {
        if (head == null) {
            return null;
        }
        Map<Node, Node> map = new HashMap<>();
        Node curr = head;
        while (curr != null) {
            map.put(curr, new Node(curr.val));
            curr = curr.next;
        }
        curr = head;
        while (curr != null) {
            map.get(curr).next = map.get(curr.next);
            map.get(curr).random = map.get(curr.random);
            curr = curr.next;
        }
        return map.get(head);
    }
}
""",
            "cpp": """#include <unordered_map>
using namespace std;

class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) {
            return nullptr;
        }
        unordered_map<Node*, Node*> map;
        Node* curr = head;
        while (curr != nullptr) {
            map[curr] = new Node(curr->val);
            curr = curr->next;
        }
        curr = head;
        while (curr != nullptr) {
            map[curr]->next = map[curr->next];
            map[curr]->random = map[curr->random];
            curr = curr->next;
        }
        return map[head];
    }
};
"""
        }
    },

    # 23. Merge k Sorted Lists
    23: {
        "name": "Brute Force (Collect and Sort)",
        "time_complexity": "O(N log N)",
        "space_complexity": "O(N)",
        "explanation": "Collect all node values from all k lists into a single vector, sort it, and build a new linked list.",
        "code": {
            "python": """class Solution:
    def mergeKLists(self, lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        values = []
        for l in lists:
            curr = l
            while curr:
                values.append(curr.val)
                curr = curr.next
        values.sort()
        dummy = ListNode(0)
        tail = dummy
        for v in values:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
""",
            "java": """import java.util.*;

class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        List<Integer> values = new ArrayList<>();
        for (ListNode l : lists) {
            ListNode curr = l;
            while (curr != null) {
                values.add(curr.val);
                curr = curr.next;
            }
        }
        Collections.sort(values);
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        for (int v : values) {
            tail.next = new ListNode(v);
            tail = tail.next;
        }
        return dummy.next;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        vector<int> values;
        for (ListNode* l : lists) {
            ListNode* curr = l;
            while (curr != nullptr) {
                values.push_back(curr->val);
                curr = curr->next;
            }
        }
        sort(values.begin(), values.end());
        ListNode dummy(0);
        ListNode* tail = &dummy;
        for (int v : values) {
            tail->next = new ListNode(v);
            tail = tail->next;
        }
        return dummy.next;
    }
};
"""
        }
    },

    # 155. Min Stack
    155: {
        "name": "Brute Force (Linear Scan on getMin)",
        "time_complexity": "Push: O(1), Pop: O(1), getMin: O(n)",
        "space_complexity": "O(n)",
        "explanation": "Use a single stack for storage. On each getMin() invocation, iterate through all elements in the stack to find the minimum value.",
        "code": {
            "python": """class MinStack:
    def __init__(self):
        self.stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)

    def pop(self) -> None:
        if self.stack:
            self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return min(self.stack)
""",
            "java": """import java.util.ArrayList;
import java.util.List;

class MinStack {
    private List<Integer> stack;

    public MinStack() {
        stack = new ArrayList<>();
    }

    public void push(int val) {
        stack.add(val);
    }

    public void pop() {
        if (!stack.isEmpty()) {
            stack.remove(stack.size() - 1);
        }
    }

    public int top() {
        return stack.get(stack.size() - 1);
    }

    public int getMin() {
        int minVal = stack.get(0);
        for (int x : stack) {
            if (x < minVal) {
                minVal = x;
            }
        }
        return minVal;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class MinStack {
private:
    vector<int> stack;

public:
    MinStack() {}

    void push(int val) {
        stack.push_back(val);
    }

    void pop() {
        if (!stack.empty()) {
            stack.pop_back();
        }
    }

    int top() {
        return stack.back();
    }

    int getMin() {
        int minVal = stack[0];
        for (int x : stack) {
            if (x < minVal) {
                minVal = x;
            }
        }
        return minVal;
    }
};
"""
        }
    },

    # 215. Kth Largest Element in an Array
    215: {
        "name": "Brute Force (Full Sort)",
        "time_complexity": "O(n log n)",
        "space_complexity": "O(1)",
        "explanation": "Sort the entire array in descending order and return the element at index k - 1.",
        "code": {
            "python": """class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        nums.sort(reverse=True)
        return nums[k - 1]
""",
            "java": """import java.util.Arrays;

class Solution {
    public int findKthLargest(int[] nums, int k) {
        Arrays.sort(nums);
        return nums[nums.length - k];
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end(), greater<int>());
        return nums[k - 1];
    }
};
"""
        }
    },

    # 226. Invert Binary Tree
    226: {
        "name": "Brute Force (Recursive Traversal Swap)",
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "explanation": "Recursively traverse each node and swap its left and right children.",
        "code": {
            "python": """class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
""",
            "java": """class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) {
            return null;
        }
        TreeNode temp = root.left;
        root.left = root.right;
        root.right = temp;
        invertTree(root.left);
        invertTree(root.right);
        return root;
    }
}
""",
            "cpp": """#include <algorithm>
using namespace std;

class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (root == nullptr) {
            return nullptr;
        }
        swap(root->left, root->right);
        invertTree(root->left);
        invertTree(root->right);
        return root;
    }
};
"""
        }
    },

    # 104. Maximum Depth of Binary Tree
    104: {
        "name": "Brute Force (Path Length Traversal)",
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "explanation": "Recursively traverse all paths from root to leaf, tracking path length and returning the maximum depth found.",
        "code": {
            "python": """class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return 1 + max(left_depth, right_depth)
""",
            "java": """class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int left = maxDepth(root.left);
        int right = maxDepth(root.right);
        return 1 + Math.max(left, right);
    }
}
""",
            "cpp": """#include <algorithm>
using namespace std;

class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }
        int left = maxDepth(root->left);
        int right = maxDepth(root->right);
        return 1 + max(left, right);
    }
};
"""
        }
    },

    # 543. Diameter of Binary Tree
    543: {
        "name": "Brute Force (Depth at Every Node)",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(h)",
        "explanation": "For every node in the tree, calculate maxDepth(left) + maxDepth(right) using independent recursive depth calls.",
        "code": {
            "python": """class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        def depth(node):
            if not node:
                return 0
            return 1 + max(depth(node.left), depth(node.right))
        current_dia = depth(root.left) + depth(root.right)
        left_dia = self.diameterOfBinaryTree(root.left)
        right_dia = self.diameterOfBinaryTree(root.right)
        return max(current_dia, left_dia, right_dia)
""",
            "java": """class Solution {
    public int diameterOfBinaryTree(TreeNode root) {
        if (root == null) {
            return 0;
        }
        int current = depth(root.left) + depth(root.right);
        int left = diameterOfBinaryTree(root.left);
        int right = diameterOfBinaryTree(root.right);
        return Math.max(current, Math.max(left, right));
    }

    private int depth(TreeNode node) {
        if (node == null) {
            return 0;
        }
        return 1 + Math.max(depth(node.left), depth(node.right));
    }
}
""",
            "cpp": """#include <algorithm>
using namespace std;

class Solution {
public:
    int diameterOfBinaryTree(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }
        int current = depth(root->left) + depth(root->right);
        int left = diameterOfBinaryTree(root->left);
        int right = diameterOfBinaryTree(root->right);
        return max(current, max(left, right));
    }

private:
    int depth(TreeNode* node) {
        if (node == nullptr) {
            return 0;
        }
        return 1 + max(depth(node->left), depth(node->right));
    }
};
"""
        }
    },

    # 102. Binary Tree Level Order Traversal
    102: {
        "name": "Brute Force (Depth-by-Depth Extraction)",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(h)",
        "explanation": "Compute tree depth, then for each level d from 1 to depth, run a separate recursive traversal to collect all nodes at level d.",
        "code": {
            "python": """class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> list[list[int]]:
        res = []
        if not root:
            return res
        def get_level(node, target_level, current_level, acc):
            if not node:
                return
            if current_level == target_level:
                acc.append(node.val)
                return
            get_level(node.left, target_level, current_level + 1, acc)
            get_level(node.right, target_level, current_level + 1, acc)

        def max_d(node):
            if not node:
                return 0
            return 1 + max(max_d(node.left), max_d(node.right))

        d = max_d(root)
        for lvl in range(1, d + 1):
            acc = []
            get_level(root, lvl, 1, acc)
            res.append(acc)
        return res
""",
            "java": """import java.util.*;

class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        if (root == null) {
            return res;
        }
        int depth = maxDepth(root);
        for (int d = 1; d <= depth; d++) {
            List<Integer> level = new ArrayList<>();
            collectLevel(root, d, 1, level);
            res.add(level);
        }
        return res;
    }

    private void collectLevel(TreeNode node, int target, int curr, List<Integer> acc) {
        if (node == null) {
            return;
        }
        if (curr == target) {
            acc.add(node.val);
            return;
        }
        collectLevel(node.left, target, curr + 1, acc);
        collectLevel(node.right, target, curr + 1, acc);
    }

    private int maxDepth(TreeNode node) {
        if (node == null) {
            return 0;
        }
        return 1 + Math.max(maxDepth(node.left), maxDepth(node.right));
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> res;
        if (root == nullptr) {
            return res;
        }
        int depth = maxDepth(root);
        for (int d = 1; d <= depth; d++) {
            vector<int> level;
            collectLevel(root, d, 1, level);
            res.push_back(level);
        }
        return res;
    }

private:
    void collectLevel(TreeNode* node, int target, int curr, vector<int>& acc) {
        if (node == nullptr) {
            return;
        }
        if (curr == target) {
            acc.push_back(node->val);
            return;
        }
        collectLevel(node->left, target, curr + 1, acc);
        collectLevel(node->right, target, curr + 1, acc);
    }

    int maxDepth(TreeNode* node) {
        if (node == nullptr) {
            return 0;
        }
        return 1 + max(maxDepth(node->left), maxDepth(node->right));
    }
};
"""
        }
    },

    # 98. Validate Binary Search Tree
    98: {
        "name": "Brute Force (Inorder Array Check)",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "explanation": "Perform an inorder traversal to collect all node values into an array, then verify that the array is strictly strictly increasing.",
        "code": {
            "python": """class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        values = []
        def inorder(node):
            if not node:
                return
            inorder(node.left)
            values.append(node.val)
            inorder(node.right)
        inorder(root)
        for i in range(1, len(values)):
            if values[i] <= values[i - 1]:
                return False
        return True
""",
            "java": """import java.util.*;

class Solution {
    public boolean isValidBST(TreeNode root) {
        List<Integer> values = new ArrayList<>();
        inorder(root, values);
        for (int i = 1; i < values.size(); i++) {
            if (values.get(i) <= values.get(i - 1)) {
                return false;
            }
        }
        return true;
    }

    private void inorder(TreeNode node, List<Integer> values) {
        if (node == null) {
            return;
        }
        inorder(node.left, values);
        values.add(node.val);
        inorder(node.right, values);
    }
}
""",
            "cpp": """#include <vector>
using namespace std;

class Solution {
public:
    bool isValidBST(TreeNode* root) {
        vector<int> values;
        inorder(root, values);
        for (size_t i = 1; i < values.size(); i++) {
            if (values[i] <= values[i - 1]) {
                return false;
            }
        }
        return true;
    }

private:
    void inorder(TreeNode* node, vector<int>& values) {
        if (node == nullptr) {
            return;
        }
        inorder(node->left, values);
        values.push_back(node->val);
        inorder(node->right, values);
    }
};
"""
        }
    },

    # 235. Lowest Common Ancestor of a Binary Search Tree
    235: {
        "name": "Brute Force (Path Intersection)",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "explanation": "Find the path from root to p and root to q as lists of nodes, then find the last common node along both paths.",
        "code": {
            "python": """class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        path_p = []
        curr = root
        while curr:
            path_p.append(curr)
            if p.val < curr.val:
                curr = curr.left
            elif p.val > curr.val:
                curr = curr.right
            else:
                break
        path_q = []
        curr = root
        while curr:
            path_q.append(curr)
            if q.val < curr.val:
                curr = curr.left
            elif q.val > curr.val:
                curr = curr.right
            else:
                break
        lca = root
        for a, b in zip(path_p, path_q):
            if a is b:
                lca = a
            else:
                break
        return lca
""",
            "java": """import java.util.*;

class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        List<TreeNode> pathP = new ArrayList<>();
        TreeNode curr = root;
        while (curr != null) {
            pathP.add(curr);
            if (p.val < curr.val) {
                curr = curr.left;
            } else if (p.val > curr.val) {
                curr = curr.right;
            } else {
                break;
            }
        }

        List<TreeNode> pathQ = new ArrayList<>();
        curr = root;
        while (curr != null) {
            pathQ.add(curr);
            if (q.val < curr.val) {
                curr = curr.left;
            } else if (q.val > curr.val) {
                curr = curr.right;
            } else {
                break;
            }
        }

        TreeNode lca = root;
        int minLen = Math.min(pathP.size(), pathQ.size());
        for (int i = 0; i < minLen; i++) {
            if (pathP.get(i) == pathQ.get(i)) {
                lca = pathP.get(i);
            } else {
                break;
            }
        }
        return lca;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        vector<TreeNode*> pathP;
        TreeNode* curr = root;
        while (curr != nullptr) {
            pathP.push_back(curr);
            if (p->val < curr->val) {
                curr = curr->left;
            } else if (p->val > curr->val) {
                curr = curr->right;
            } else {
                break;
            }
        }

        vector<TreeNode*> pathQ;
        curr = root;
        while (curr != nullptr) {
            pathQ.push_back(curr);
            if (q->val < curr->val) {
                curr = curr->left;
            } else if (q->val > curr->val) {
                curr = curr->right;
            } else {
                break;
            }
        }

        TreeNode* lca = root;
        int minLen = min(pathP.size(), pathQ.size());
        for (int i = 0; i < minLen; i++) {
            if (pathP[i] == pathQ[i]) {
                lca = pathP[i];
            } else {
                break;
            }
        }
        return lca;
    }
};
"""
        }
    },

    # 236. Lowest Common Ancestor of a Binary Tree
    236: {
        "name": "Brute Force (Root-to-Node Path Finding)",
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "explanation": "Search the tree to build root-to-p and root-to-q node paths, then traverse both paths simultaneously to identify their last common ancestor.",
        "code": {
            "python": """class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        def find_path(node, target, path):
            if not node:
                return False
            path.append(node)
            if node is target:
                return True
            if find_path(node.left, target, path) or find_path(node.right, target, path):
                return True
            path.pop()
            return False

        path_p = []
        path_q = []
        find_path(root, p, path_p)
        find_path(root, q, path_q)

        lca = root
        for a, b in zip(path_p, path_q):
            if a is b:
                lca = a
            else:
                break
        return lca
""",
            "java": """import java.util.*;

class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        List<TreeNode> pathP = new ArrayList<>();
        List<TreeNode> pathQ = new ArrayList<>();
        findPath(root, p, pathP);
        findPath(root, q, pathQ);

        TreeNode lca = root;
        int minLen = Math.min(pathP.size(), pathQ.size());
        for (int i = 0; i < minLen; i++) {
            if (pathP.get(i) == pathQ.get(i)) {
                lca = pathP.get(i);
            } else {
                break;
            }
        }
        return lca;
    }

    private boolean findPath(TreeNode node, TreeNode target, List<TreeNode> path) {
        if (node == null) {
            return false;
        }
        path.add(node);
        if (node == target) {
            return true;
        }
        if (findPath(node.left, target, path) || findPath(node.right, target, path)) {
            return true;
        }
        path.remove(path.size() - 1);
        return false;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        vector<TreeNode*> pathP;
        vector<TreeNode*> pathQ;
        findPath(root, p, pathP);
        findPath(root, q, pathQ);

        TreeNode* lca = root;
        int minLen = min(pathP.size(), pathQ.size());
        for (int i = 0; i < minLen; i++) {
            if (pathP[i] == pathQ[i]) {
                lca = pathP[i];
            } else {
                break;
            }
        }
        return lca;
    }

private:
    bool findPath(TreeNode* node, TreeNode* target, vector<TreeNode*>& path) {
        if (node == nullptr) {
            return false;
        }
        path.push_back(node);
        if (node == target) {
            return true;
        }
        if (findPath(node->left, target, path) || findPath(node->right, target, path)) {
            return true;
        }
        path.pop_back();
        return false;
    }
};
"""
        }
    },

    # 105. Construct Binary Tree from Preorder and Inorder Traversal
    105: {
        "name": "Brute Force (Linear Inorder Search)",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(n)",
        "explanation": "At each step, take the root from preorder, search for its position in inorder linearly, and partition the subarrays recursively.",
        "code": {
            "python": """class Solution:
    def buildTree(self, preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
        if not preorder or not inorder:
            return None
        root_val = preorder[0]
        root = TreeNode(root_val)
        mid = inorder.index(root_val)
        root.left = self.buildTree(preorder[1 : mid + 1], inorder[:mid])
        root.right = self.buildTree(preorder[mid + 1 :], inorder[mid + 1 :])
        return root
""",
            "java": """import java.util.Arrays;

class Solution {
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder.length == 0 || inorder.length == 0) {
            return null;
        }
        int rootVal = preorder[0];
        TreeNode root = new TreeNode(rootVal);
        int mid = -1;
        for (int i = 0; i < inorder.length; i++) {
            if (inorder[i] == rootVal) {
                mid = i;
                break;
            }
        }
        int[] leftPre = Arrays.copyOfRange(preorder, 1, mid + 1);
        int[] leftIn = Arrays.copyOfRange(inorder, 0, mid);
        int[] rightPre = Arrays.copyOfRange(preorder, mid + 1, preorder.length);
        int[] rightIn = Arrays.copyOfRange(inorder, mid + 1, inorder.length);

        root.left = buildTree(leftPre, leftIn);
        root.right = buildTree(rightPre, rightIn);
        return root;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        if (preorder.empty() || inorder.empty()) {
            return nullptr;
        }
        int rootVal = preorder[0];
        TreeNode* root = new TreeNode(rootVal);
        int mid = 0;
        for (int i = 0; i < (int)inorder.size(); i++) {
            if (inorder[i] == rootVal) {
                mid = i;
                break;
            }
        }
        vector<int> leftPre(preorder.begin() + 1, preorder.begin() + 1 + mid);
        vector<int> leftIn(inorder.begin(), inorder.begin() + mid);
        vector<int> rightPre(preorder.begin() + 1 + mid, preorder.end());
        vector<int> rightIn(inorder.begin() + mid + 1, inorder.end());

        root->left = buildTree(leftPre, leftIn);
        root->right = buildTree(rightPre, rightIn);
        return root;
    }
};
"""
        }
    },

    # 124. Binary Tree Maximum Path Sum
    124: {
        "name": "Brute Force (All Node Pairs Path Sum)",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(h)",
        "explanation": "For each node, compute the maximum downward branch sum through left and right subtrees and update the global maximum path sum.",
        "code": {
            "python": """class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float('-inf')
        def max_gain(node):
            if not node:
                return 0
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)
            price_newpath = node.val + left_gain + right_gain
            if price_newpath > self.max_sum:
                self.max_sum = price_newpath
            return node.val + max(left_gain, right_gain)
        max_gain(root)
        return int(self.max_sum)
""",
            "java": """class Solution {
    private int maxSum = Integer.MIN_VALUE;

    public int maxPathSum(TreeNode root) {
        maxGain(root);
        return maxSum;
    }

    private int maxGain(TreeNode node) {
        if (node == null) {
            return 0;
        }
        int leftGain = Math.max(maxGain(node.left), 0);
        int rightGain = Math.max(maxGain(node.right), 0);
        int pathSum = node.val + leftGain + rightGain;
        if (pathSum > maxSum) {
            maxSum = pathSum;
        }
        return node.val + Math.max(leftGain, rightGain);
    }
}
""",
            "cpp": """#include <algorithm>
#include <climits>
using namespace std;

class Solution {
private:
    int maxSum = INT_MIN;

    int maxGain(TreeNode* node) {
        if (node == nullptr) {
            return 0;
        }
        int leftGain = max(maxGain(node->left), 0);
        int rightGain = max(maxGain(node->right), 0);
        int pathSum = node->val + leftGain + rightGain;
        if (pathSum > maxSum) {
            maxSum = pathSum;
        }
        return node->val + max(leftGain, rightGain);
    }

public:
    int maxPathSum(TreeNode* root) {
        maxGain(root);
        return maxSum;
    }
};
"""
        }
    },

    # 994. Rotting Oranges
    994: {
        "name": "Brute Force (Minute-by-Minute Simulation)",
        "time_complexity": "O((m * n)^2)",
        "space_complexity": "O(m * n)",
        "explanation": "Simulate minute by minute: scan the entire grid on each tick to find fresh oranges adjacent to rotten ones, mark them rotten, and repeat until no more changes occur.",
        "code": {
            "python": """class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        R, C = len(grid), len(grid[0])
        minutes = 0
        while True:
            to_rot = []
            for r in range(R):
                for c in range(C):
                    if grid[r][c] == 1:
                        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 2:
                                to_rot.append((r, c))
                                break
            if not to_rot:
                break
            for r, c in to_rot:
                grid[r][c] = 2
            minutes += 1

        for r in range(R):
            for c in range(C):
                if grid[r][c] == 1:
                    return -1
        return minutes
""",
            "java": """import java.util.*;

class Solution {
    public int orangesRotting(int[][] grid) {
        int R = grid.length;
        int C = grid[0].length;
        int minutes = 0;
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        while (true) {
            List<int[]> toRot = new ArrayList<>();
            for (int r = 0; r < R; r++) {
                for (int c = 0; c < C; c++) {
                    if (grid[r][c] == 1) {
                        for (int[] d : dirs) {
                            int nr = r + d[0];
                            int nc = c + d[1];
                            if (nr >= 0 && nr < R && nc >= 0 && nc < C && grid[nr][nc] == 2) {
                                toRot.add(new int[]{r, c});
                                break;
                            }
                        }
                    }
                }
            }
            if (toRot.isEmpty()) {
                break;
            }
            for (int[] cell : toRot) {
                grid[cell[0]][cell[1]] = 2;
            }
            minutes++;
        }

        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                if (grid[r][c] == 1) {
                    return -1;
                }
            }
        }
        return minutes;
    }
}
""",
            "cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        int R = grid.size();
        int C = grid[0].size();
        int minutes = 0;
        vector<pair<int, int>> dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        while (true) {
            vector<pair<int, int>> toRot;
            for (int r = 0; r < R; r++) {
                for (int c = 0; c < C; c++) {
                    if (grid[r][c] == 1) {
                        for (auto& d : dirs) {
                            int nr = r + d.first;
                            int nc = c + d.second;
                            if (nr >= 0 && nr < R && nc >= 0 && nc < C && grid[nr][nc] == 2) {
                                toRot.push_back({r, c});
                                break;
                            }
                        }
                    }
                }
            }
            if (toRot.empty()) {
                break;
            }
            for (auto& p : toRot) {
                grid[p.first][p.second] = 2;
            }
            minutes++;
        }

        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                if (grid[r][c] == 1) {
                    return -1;
                }
            }
        }
        return minutes;
    }
};
"""
        }
    },

    # 417. Pacific Atlantic Water Flow
    417: {
        "name": "Brute Force (DFS From Every Cell)",
        "time_complexity": "O((m * n)^2)",
        "space_complexity": "O(m * n)",
        "explanation": "From every single cell (r, c), run a dedicated DFS traversal to check whether water can flow downwards to reach both the Pacific and Atlantic oceans.",
        "code": {
            "python": """class Solution:
    def pacificAtlantic(self, heights: list[list[int]]) -> list[list[int]]:
        R, C = len(heights), len(heights[0])
        res = []
        for r in range(R):
            for c in range(C):
                visited = set()
                reach_p = [False]
                reach_a = [False]
                def dfs(cr, cc):
                    if cr == 0 or cc == 0:
                        reach_p[0] = True
                    if cr == R - 1 or cc == C - 1:
                        reach_a[0] = True
                    if reach_p[0] and reach_a[0]:
                        return
                    visited.add((cr, cc))
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in visited:
                            if heights[nr][nc] <= heights[cr][cc]:
                                dfs(nr, nc)
                dfs(r, c)
                if reach_p[0] and reach_a[0]:
                    res.append([r, c])
        return res
""",
            "java": """import java.util.*;

class Solution {
    public List<List<Integer>> pacificAtlantic(int[][] heights) {
        int R = heights.length;
        int C = heights[0].length;
        List<List<Integer>> res = new ArrayList<>();

        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                boolean[] reach = new boolean[2]; // [0]: Pacific, [1]: Atlantic
                boolean[][] visited = new boolean[R][C];
                dfs(heights, r, c, reach, visited, R, C);
                if (reach[0] && reach[1]) {
                    res.add(Arrays.asList(r, c));
                }
            }
        }
        return res;
    }

    private void dfs(int[][] heights, int r, int c, boolean[] reach, boolean[][] visited, int R, int C) {
        if (r == 0 || c == 0) {
            reach[0] = true;
        }
        if (r == R - 1 || c == C - 1) {
            reach[1] = true;
        }
        if (reach[0] && reach[1]) {
            return;
        }
        visited[r][c] = true;
        int[][] dirs = {{-1,0},{1,0},{0,-1},{0,1}};
        for (int[] d : dirs) {
            int nr = r + d[0];
            int nc = c + d[1];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && !visited[nr][nc]) {
                if (heights[nr][nc] <= heights[r][c]) {
                    dfs(heights, nr, nc, reach, visited, R, C);
                }
            }
        }
    }
}
""",
            "cpp": """#include <vector>
using namespace std;

class Solution {
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        int R = heights.size();
        int C = heights[0].size();
        vector<vector<int>> res;

        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                bool reachP = false;
                bool reachA = false;
                vector<vector<bool>> visited(R, vector<bool>(C, false));
                dfs(heights, r, c, reachP, reachA, visited, R, C);
                if (reachP && reachA) {
                    res.push_back({r, c});
                }
            }
        }
        return res;
    }

private:
    void dfs(vector<vector<int>>& heights, int r, int c, bool& reachP, bool& reachA, vector<vector<bool>>& visited, int R, int C) {
        if (r == 0 || c == 0) {
            reachP = true;
        }
        if (r == R - 1 || c == C - 1) {
            reachA = true;
        }
        if (reachP && reachA) {
            return;
        }
        visited[r][c] = true;
        int dirs[4][2] = {{-1,0},{1,0},{0,-1},{0,1}};
        for (auto& d : dirs) {
            int nr = r + d[0];
            int nc = c + d[1];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && !visited[nr][nc]) {
                if (heights[nr][nc] <= heights[r][c]) {
                    dfs(heights, nr, nc, reachP, reachA, visited, R, C);
                }
            }
        }
    }
};
"""
        }
    },

    # 743. Network Delay Time
    743: {
        "name": "Brute Force (Bellman-Ford Relaxation)",
        "time_complexity": "O(V * E)",
        "space_complexity": "O(V)",
        "explanation": "Run Bellman-Ford by relaxing all directed edges in the network n - 1 times to find shortest paths from k to all nodes.",
        "code": {
            "python": """class Solution:
    def networkDelayTime(self, times: list[list[int]], n: int, k: int) -> int:
        dist = [float('inf')] * (n + 1)
        dist[k] = 0
        for _ in range(n - 1):
            for u, v, w in times:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        max_d = max(dist[1:])
        return int(max_d) if max_d != float('inf') else -1
""",
            "java": """import java.util.Arrays;

class Solution {
    public int networkDelayTime(int[][] times, int n, int k) {
        int[] dist = new int[n + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[k] = 0;

        for (int i = 1; i <= n - 1; i++) {
            for (int[] edge : times) {
                int u = edge[0];
                int v = edge[1];
                int w = edge[2];
                if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }
        int maxDist = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == Integer.MAX_VALUE) {
                return -1;
            }
            if (dist[i] > maxDist) {
                maxDist = dist[i];
            }
        }
        return maxDist;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<int> dist(n + 1, INT_MAX);
        dist[k] = 0;

        for (int i = 1; i <= n - 1; i++) {
            for (const auto& edge : times) {
                int u = edge[0];
                int v = edge[1];
                int w = edge[2];
                if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }
        int maxDist = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == INT_MAX) {
                return -1;
            }
            if (dist[i] > maxDist) {
                maxDist = dist[i];
            }
        }
        return maxDist;
    }
};
"""
        }
    },
}

with open("backend/app/curated_brute_codes.py", "r", encoding="utf-8") as f:
    content = f.read()

# Merge into content
import sys
sys.path.insert(0, '.')
from backend.app.curated_brute_codes import CURATED_BRUTE_FORCE

# Update CURATED_BRUTE_FORCE with MORE_BRUTES
CURATED_BRUTE_FORCE.update(MORE_BRUTES)

with open("backend/app/curated_brute_codes.py", "w", encoding="utf-8") as f:
    f.write('"""Curated brute force approaches dictionary"""\n\nCURATED_BRUTE_FORCE = ' + repr(CURATED_BRUTE_FORCE) + '\n')

print(f"Successfully updated curated_brute_codes.py with total {len(CURATED_BRUTE_FORCE)} entries!")
