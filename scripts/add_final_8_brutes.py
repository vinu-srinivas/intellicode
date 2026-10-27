# scripts/add_final_8_brutes.py
import json
import sys
sys.path.insert(0, '.')
from scripts.apply_all_curations import format_c_code

FINAL_8 = {
    # 5. Longest Palindromic Substring
    5: {
        "name": "Brute Force (Check All Substrings)",
        "time_complexity": "O(n^3)",
        "space_complexity": "O(1)",
        "explanation": "Iterate through every possible substring (i, j) with nested loops and check whether the substring is a palindrome, tracking the longest palindrome found.",
        "code": {
            "python": """class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n <= 1:
            return s
        longest = s[0]
        for i in range(n):
            for j in range(i + 1, n + 1):
                sub = s[i:j]
                if sub == sub[::-1] and len(sub) > len(longest):
                    longest = sub
        return longest
""",
            "java": """class Solution {
    public String longestPalindrome(String s) {
        int n = s.length();
        if (n <= 1) {
            return s;
        }
        String longest = s.substring(0, 1);
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j <= n; j++) {
                String sub = s.substring(i, j);
                if (isPal(sub) && sub.length() > longest.length()) {
                    longest = sub;
                }
            }
        }
        return longest;
    }

    private boolean isPal(String sub) {
        int l = 0;
        int r = sub.length() - 1;
        while (l < r) {
            if (sub.charAt(l) != sub.charAt(r)) {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
}
""",
            "cpp": """#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    string longestPalindrome(string s) {
        int n = s.length();
        if (n <= 1) {
            return s;
        }
        string longest = s.substr(0, 1);
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j <= n; j++) {
                string sub = s.substr(i, j - i);
                if (isPal(sub) && sub.length() > longest.length()) {
                    longest = sub;
                }
            }
        }
        return longest;
    }

private:
    bool isPal(const string& sub) {
        int l = 0;
        int r = sub.length() - 1;
        while (l < r) {
            if (sub[l] != sub[r]) {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
"""
        }
    },

    # 150. Evaluate Reverse Polish Notation
    150: {
        "name": "Brute Force (Array Contraction)",
        "time_complexity": "O(n^2)",
        "space_complexity": "O(n)",
        "explanation": "Repeatedly scan the list for an operator preceded by two numbers, calculate the result, replace the three tokens with the result, and repeat until one token remains.",
        "code": {
            "python": """class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        cur = list(tokens)
        while len(cur) > 1:
            for i in range(len(cur)):
                if cur[i] in ["+", "-", "*", "/"]:
                    a = int(cur[i - 2])
                    b = int(cur[i - 1])
                    op = cur[i]
                    if op == "+":
                        val = a + b
                    elif op == "-":
                        val = a - b
                    elif op == "*":
                        val = a * b
                    else:
                        val = int(a / b)
                    cur = cur[:i - 2] + [str(val)] + cur[i + 1:]
                    break
        return int(cur[0])
""",
            "java": """import java.util.*;

class Solution {
    public int evalRPN(String[] tokens) {
        List<String> cur = new ArrayList<>(Arrays.asList(tokens));
        while (cur.size() > 1) {
            for (int i = 0; i < cur.size(); i++) {
                String token = cur.get(i);
                if (token.equals("+") || token.equals("-") || token.equals("*") || token.equals("/")) {
                    int a = Integer.parseInt(cur.get(i - 2));
                    int b = Integer.parseInt(cur.get(i - 1));
                    int val = 0;
                    if (token.equals("+")) {
                        val = a + b;
                    } else if (token.equals("-")) {
                        val = a - b;
                    } else if (token.equals("*")) {
                        val = a * b;
                    } else {
                        val = a / b;
                    }
                    cur.remove(i);
                    cur.remove(i - 1);
                    cur.set(i - 2, String.valueOf(val));
                    break;
                }
            }
        }
        return Integer.parseInt(cur.get(0));
    }
}
""",
            "cpp": """#include <vector>
#include <string>
using namespace std;

class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        vector<string> cur = tokens;
        while (cur.size() > 1) {
            for (int i = 0; i < (int)cur.size(); i++) {
                string token = cur[i];
                if (token == "+" || token == "-" || token == "*" || token == "/") {
                    int a = stoi(cur[i - 2]);
                    int b = stoi(cur[i - 1]);
                    int val = 0;
                    if (token == "+") {
                        val = a + b;
                    } else if (token == "-") {
                        val = a - b;
                    } else if (token == "*") {
                        val = a * b;
                    } else {
                        val = a / b;
                    }
                    cur.erase(cur.begin() + i);
                    cur.erase(cur.begin() + i - 1);
                    cur[i - 2] = to_string(val);
                    break;
                }
            }
        }
        return stoi(cur[0]);
    }
};
"""
        }
    },

    # 853. Car Fleet
    853: {
        "name": "Brute Force (Pairwise Catch-Up Check)",
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "explanation": "Sort cars descending by position. For each lead car, check if trailing cars catch up by computing their time to target, combining fleets whenever a trailing car arrives earlier or at the same time.",
        "code": {
            "python": """class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        n = len(position)
        if n <= 1:
            return n
        cars = sorted(zip(position, speed), reverse=True)
        fleets = 0
        lead_time = 0.0
        for pos, spd in cars:
            time = (target - pos) / spd
            if time > lead_time:
                fleets += 1
                lead_time = time
        return fleets
""",
            "java": """import java.util.*;

class Solution {
    public int carFleet(int target, int[] position, int[] speed) {
        int n = position.length;
        if (n <= 1) {
            return n;
        }
        double[][] cars = new double[n][2];
        for (int i = 0; i < n; i++) {
            cars[i][0] = position[i];
            cars[i][1] = (double)(target - position[i]) / speed[i];
        }
        Arrays.sort(cars, (a, b) -> Double.compare(b[0], a[0]));

        int fleets = 0;
        double leadTime = 0.0;
        for (int i = 0; i < n; i++) {
            double time = cars[i][1];
            if (time > leadTime) {
                fleets++;
                leadTime = time;
            }
        }
        return fleets;
    }
}
""",
            "cpp": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        int n = position.size();
        if (n <= 1) {
            return n;
        }
        vector<pair<int, double>> cars(n);
        for (int i = 0; i < n; i++) {
            cars[i] = {position[i], (double)(target - position[i]) / speed[i]};
        }
        sort(cars.begin(), cars.end(), [](const pair<int, double>& a, const pair<int, double>& b) {
            return a.first > b.first;
        });

        int fleets = 0;
        double leadTime = 0.0;
        for (int i = 0; i < n; i++) {
            double time = cars[i].second;
            if (time > leadTime) {
                fleets++;
                leadTime = time;
            }
        }
        return fleets;
    }
};
"""
        }
    },

    # 200. Number of Islands
    200: {
        "name": "Brute Force (Visited Matrix Traversal)",
        "time_complexity": "O(m * n)",
        "space_complexity": "O(m * n)",
        "explanation": "Maintain an explicit external visited matrix without mutating input. For every unvisited '1', trigger BFS/DFS to mark the entire component as visited and increment island count.",
        "code": {
            "python": """class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        if not grid:
            return 0
        R, C = len(grid), len(grid[0])
        visited = [[False] * C for _ in range(R)]
        islands = 0

        def dfs(r, c):
            if r < 0 or r >= R or c < 0 or c >= C or grid[r][c] != '1' or visited[r][c]:
                return
            visited[r][c] = True
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        for r in range(R):
            for c in range(C):
                if grid[r][c] == '1' and not visited[r][c]:
                    islands += 1
                    dfs(r, c)
        return islands
""",
            "java": """class Solution {
    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0) {
            return 0;
        }
        int R = grid.length;
        int C = grid[0].length;
        boolean[][] visited = new boolean[R][C];
        int islands = 0;

        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                if (grid[r][c] == '1' && !visited[r][c]) {
                    islands++;
                    dfs(grid, r, c, visited, R, C);
                }
            }
        }
        return islands;
    }

    private void dfs(char[][] grid, int r, int c, boolean[][] visited, int R, int C) {
        if (r < 0 || r >= R || c < 0 || c >= C || grid[r][c] != '1' || visited[r][c]) {
            return;
        }
        visited[r][c] = true;
        dfs(grid, r + 1, c, visited, R, C);
        dfs(grid, r - 1, c, visited, R, C);
        dfs(grid, r, c + 1, visited, R, C);
        dfs(grid, r, c - 1, visited, R, C);
    }
}
""",
            "cpp": """#include <vector>
using namespace std;

class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        if (grid.empty()) {
            return 0;
        }
        int R = grid.size();
        int C = grid[0].size();
        vector<vector<bool>> visited(R, vector<bool>(C, false));
        int islands = 0;

        for (int r = 0; r < R; r++) {
            for (int c = 0; c < C; c++) {
                if (grid[r][c] == '1' && !visited[r][c]) {
                    islands++;
                    dfs(grid, r, c, visited, R, C);
                }
            }
        }
        return islands;
    }

private:
    void dfs(vector<vector<char>>& grid, int r, int c, vector<vector<bool>>& visited, int R, int C) {
        if (r < 0 || r >= R || c < 0 || c >= C || grid[r][c] != '1' || visited[r][c]) {
            return;
        }
        visited[r][c] = true;
        dfs(grid, r + 1, c, visited, R, C);
        dfs(grid, r - 1, c, visited, R, C);
        dfs(grid, r, c + 1, visited, R, C);
        dfs(grid, r, c - 1, visited, R, C);
    }
};
"""
        }
    },

    # 133. Clone Graph
    133: {
        "name": "Brute Force (Two-Pass Clone & Link)",
        "time_complexity": "O(V^2 + E)",
        "space_complexity": "O(V)",
        "explanation": "Collect all nodes in pass 1 and instantiate clone nodes into a list. In pass 2, for each node, search the list to link clone neighbors.",
        "code": {
            "python": """class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None
        clones = {}
        def get_all(curr):
            if curr in clones:
                return
            clones[curr] = Node(curr.val)
            for neighbor in curr.neighbors:
                get_all(neighbor)
        get_all(node)
        for original, clone in clones.items():
            for neighbor in original.neighbors:
                clone.neighbors.append(clones[neighbor])
        return clones[node]
""",
            "java": """import java.util.*;

class Solution {
    public Node cloneGraph(Node node) {
        if (node == null) {
            return null;
        }
        Map<Node, Node> map = new HashMap<>();
        collect(node, map);
        for (Map.Entry<Node, Node> entry : map.entrySet()) {
            for (Node neighbor : entry.getKey().neighbors) {
                entry.getValue().neighbors.add(map.get(neighbor));
            }
        }
        return map.get(node);
    }

    private void collect(Node curr, Map<Node, Node> map) {
        if (map.containsKey(curr)) {
            return;
        }
        map.put(curr, new Node(curr.val));
        for (Node neighbor : curr.neighbors) {
            collect(neighbor, map);
        }
    }
}
""",
            "cpp": """#include <unordered_map>
#include <vector>
using namespace std;

class Solution {
public:
    Node* cloneGraph(Node* node) {
        if (!node) {
            return nullptr;
        }
        unordered_map<Node*, Node*> clones;
        collect(node, clones);
        for (auto& pair : clones) {
            for (Node* neighbor : pair.first->neighbors) {
                pair.second->neighbors.push_back(clones[neighbor]);
            }
        }
        return clones[node];
    }

private:
    void collect(Node* curr, unordered_map<Node*, Node*>& clones) {
        if (clones.count(curr)) {
            return;
        }
        clones[curr] = new Node(curr->val);
        for (Node* neighbor : curr->neighbors) {
            collect(neighbor, clones);
        }
    }
};
"""
        }
    },

    # 207. Course Schedule
    207: {
        "name": "Brute Force (DFS Cycle Check From Each Node)",
        "time_complexity": "O(V * (V + E))",
        "space_complexity": "O(V + E)",
        "explanation": "From every course i, perform an independent full depth-first search to check whether any chain of prerequisites cycles back to course i.",
        "code": {
            "python": """class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        adj = [[] for _ in range(numCourses)]
        for dest, src in prerequisites:
            adj[src].append(dest)

        for start in range(numCourses):
            visited = set()
            stack = [start]
            while stack:
                curr = stack.pop()
                for neighbor in adj[curr]:
                    if neighbor == start:
                        return False
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
        return True
""",
            "java": """import java.util.*;

class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            adj.add(new ArrayList<>());
        }
        for (int[] edge : prerequisites) {
            adj.get(edge[1]).add(edge[0]);
        }

        for (int start = 0; start < numCourses; start++) {
            boolean[] visited = new boolean[numCourses];
            Queue<Integer> q = new LinkedList<>();
            q.add(start);
            while (!q.isEmpty()) {
                int curr = q.poll();
                for (int next : adj.get(curr)) {
                    if (next == start) {
                        return false;
                    }
                    if (!visited[next]) {
                        visited[next] = true;
                        q.add(next);
                    }
                }
            }
        }
        return true;
    }
}
""",
            "cpp": """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        for (const auto& edge : prerequisites) {
            adj[edge[1]].push_back(edge[0]);
        }

        for (int start = 0; start < numCourses; start++) {
            vector<bool> visited(numCourses, false);
            queue<int> q;
            q.push(start);
            while (!q.empty()) {
                int curr = q.front();
                q.pop();
                for (int next : adj[curr]) {
                    if (next == start) {
                        return false;
                    }
                    if (!visited[next]) {
                        visited[next] = true;
                        q.push(next);
                    }
                }
            }
        }
        return true;
    }
};
"""
        }
    },

    # 210. Course Schedule II
    210: {
        "name": "Brute Force (Sequential Prerequisite Verification)",
        "time_complexity": "O(V^2 + E)",
        "space_complexity": "O(V + E)",
        "explanation": "Repeatedly scan the remaining courses to find one whose prerequisites have all been fulfilled. Append it to the order and repeat until all courses are taken or stuck in a cycle.",
        "code": {
            "python": """class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        prereqs = {i: set() for i in range(numCourses)}
        for dest, src in prerequisites:
            prereqs[dest].add(src)

        order = []
        completed = set()
        for _ in range(numCourses):
            found = False
            for c in range(numCourses):
                if c not in completed and prereqs[c].issubset(completed):
                    order.append(c)
                    completed.add(c)
                    found = True
                    break
            if not found:
                return []
        return order
""",
            "java": """import java.util.*;

class Solution {
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        List<Set<Integer>> prereqs = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) {
            prereqs.add(new HashSet<>());
        }
        for (int[] edge : prerequisites) {
            prereqs.get(edge[0]).add(edge[1]);
        }

        int[] order = new int[numCourses];
        boolean[] completed = new boolean[numCourses];
        int count = 0;

        for (int step = 0; step < numCourses; step++) {
            boolean found = false;
            for (int c = 0; c < numCourses; c++) {
                if (!completed[c]) {
                    boolean allDone = true;
                    for (int p : prereqs.get(c)) {
                        if (!completed[p]) {
                            allDone = false;
                            break;
                        }
                    }
                    if (allDone) {
                        order[count++] = c;
                        completed[c] = true;
                        found = true;
                        break;
                    }
                }
            }
            if (!found) {
                return new int[0];
            }
        }
        return order;
    }
}
""",
            "cpp": """#include <vector>
#include <unordered_set>
using namespace std;

class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        vector<unordered_set<int>> prereqs(numCourses);
        for (const auto& edge : prerequisites) {
            prereqs[edge[0]].insert(edge[1]);
        }

        vector<int> order;
        vector<bool> completed(numCourses, false);

        for (int step = 0; step < numCourses; step++) {
            bool found = false;
            for (int c = 0; c < numCourses; c++) {
                if (!completed[c]) {
                    bool allDone = true;
                    for (int p : prereqs[c]) {
                        if (!completed[p]) {
                            allDone = false;
                            break;
                        }
                    }
                    if (allDone) {
                        order.push_back(c);
                        completed[c] = true;
                        found = true;
                        break;
                    }
                }
            }
            if (!found) {
                return {};
            }
        }
        return order;
    }
};
"""
        }
    },

    # 785. Is Graph Bipartite?
    785: {
        "name": "Brute Force (Two-Coloring DFS Verification)",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "explanation": "Color each unvisited node and verify that all connected neighbors can alternate colors without any collision.",
        "code": {
            "python": """class Solution:
    def isBipartite(self, graph: list[list[int]]) -> bool:
        n = len(graph)
        color = {}
        for start in range(n):
            if start not in color:
                stack = [start]
                color[start] = 0
                while stack:
                    curr = stack.pop()
                    for neighbor in graph[curr]:
                        if neighbor not in color:
                            color[neighbor] = 1 - color[curr]
                            stack.append(neighbor)
                        elif color[neighbor] == color[curr]:
                            return False
        return True
""",
            "java": """import java.util.*;

class Solution {
    public boolean isBipartite(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        Arrays.fill(color, -1);

        for (int start = 0; start < n; start++) {
            if (color[start] == -1) {
                Queue<Integer> q = new LinkedList<>();
                q.add(start);
                color[start] = 0;
                while (!q.isEmpty()) {
                    int curr = q.poll();
                    for (int neighbor : graph[curr]) {
                        if (color[neighbor] == -1) {
                            color[neighbor] = 1 - color[curr];
                            q.add(neighbor);
                        } else if (color[neighbor] == color[curr]) {
                            return false;
                        }
                    }
                }
            }
        }
        return true;
    }
}
""",
            "cpp": """#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    bool isBipartite(vector<vector<int>>& graph) {
        int n = graph.size();
        vector<int> color(n, -1);

        for (int start = 0; start < n; start++) {
            if (color[start] == -1) {
                queue<int> q;
                q.push(start);
                color[start] = 0;
                while (!q.empty()) {
                    int curr = q.front();
                    q.pop();
                    for (int neighbor : graph[curr]) {
                        if (color[neighbor] == -1) {
                            color[neighbor] = 1 - color[curr];
                            q.push(neighbor);
                        } else if (color[neighbor] == color[curr]) {
                            return false;
                        }
                    }
                }
            }
        }
        return true;
    }
};
"""
        }
    },
}

with open("codebase.json", "r", encoding="utf-8") as f:
    db = json.load(f)

for p in db["problems"]:
    pid = p["leetcode_id"]
    if pid in FINAL_8:
        curated_bf = FINAL_8[pid]
        approaches = p.get("approaches", [])
        
        new_app = {
            "name": curated_bf["name"],
            "idea": curated_bf["explanation"],
            "complexity": f"Time: {curated_bf['time_complexity']}, Space: {curated_bf['space_complexity']}",
            "explanation": curated_bf["explanation"],
            "code": {
                "python": curated_bf["code"]["python"],
                "java": format_c_code(curated_bf["code"]["java"]),
                "cpp": format_c_code(curated_bf["code"]["cpp"]),
            }
        }
        
        bf_idx = -1
        for idx, app in enumerate(approaches):
            if "brute" in app.get("name", "").lower():
                bf_idx = idx
                break
                
        if bf_idx != -1:
            approaches[bf_idx] = new_app
        else:
            approaches.insert(0, new_app)
            
        p["approaches"] = approaches

with open("codebase.json", "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Applied final 8 brutes successfully!")
