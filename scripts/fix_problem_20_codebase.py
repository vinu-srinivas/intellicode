import json

with open("codebase.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for p in data["problems"]:
    if p["leetcode_id"] == 20:
        p["primary_solution"]["code"]["java"] = """import java.util.*;

class Solution {
    public boolean isValid(String s) {
        Map<Character, Character> p = new HashMap<>();
        p.put(')', '(');
        p.put('}', '{');
        p.put(']', '[');
        Deque<Character> st = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (p.containsKey(c)) {
                if (st.isEmpty() || st.pop() != p.get(c)) return false;
            } else {
                st.push(c);
            }
        }
        return st.isEmpty();
    }
}
"""
        p["primary_solution"]["code"]["cpp"] = """#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    bool isValid(string s) {
        unordered_map<char, char> p = {
            {')', '('},
            {']', '['},
            {'}', '{'}
        };
        vector<char> st;
        for (char c : s) {
            if (p.count(c)) {
                if (st.empty() || st.back() != p[c]) return false;
                st.pop_back();
            } else {
                st.push_back(c);
            }
        }
        return st.empty();
    }
};
"""

with open("codebase.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Problem 20 solutions updated cleanly in codebase.json")
