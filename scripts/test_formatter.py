import re

def format_c_style_code(code: str) -> str:
    """Format Java / C++ code with proper indentation and explicit curly braces for all control blocks."""
    lines = code.split("\n")
    cleaned_lines = []
    
    # First pass: preserve includes and comments, but normalize single-line crammed blocks
    for line in lines:
        s = line.strip()
        if not s:
            cleaned_lines.append("")
            continue
        if s.startswith("#") or s.startswith("//") or s.startswith("/*") or s.startswith("*"):
            cleaned_lines.append(s)
            continue
        
        # Check if line has multiple statements crammed together e.g. "for(int p:prices){ mn=min(mn,p); best=max(best,p-mn); }"
        # or "int[] ans=new int[k];for(int i=k-1;i>=0;i--)ans[i]=pq.poll()[0];return ans;"
        # We can split on ';' and '{' and '}' carefully
        parts = []
        cur = []
        in_paren = 0
        in_str = False
        in_char = False
        escape = False
        
        for ch in s:
            if escape:
                cur.append(ch)
                escape = False
                continue
            if ch == '\\':
                cur.append(ch)
                escape = True
                continue
            if ch == '"' and not in_char:
                in_str = not in_str
                cur.append(ch)
                continue
            if ch == "'" and not in_str:
                in_char = not in_char
                cur.append(ch)
                continue
            if in_str or in_char:
                cur.append(ch)
                continue
                
            if ch == '(':
                in_paren += 1
                cur.append(ch)
            elif ch == ')':
                in_paren -= 1
                cur.append(ch)
            elif ch == '{' and in_paren == 0:
                cur_s = "".join(cur).strip()
                if cur_s:
                    parts.append(cur_s + " {")
                else:
                    parts.append("{")
                cur = []
            elif ch == '}' and in_paren == 0:
                cur_s = "".join(cur).strip()
                if cur_s:
                    parts.append(cur_s)
                parts.append("}")
                cur = []
            elif ch == ';' and in_paren == 0:
                cur.append(ch)
                parts.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
                
        rem = "".join(cur).strip()
        if rem:
            parts.append(rem)
            
        for p in parts:
            if p:
                cleaned_lines.append(p)
                
    # Second pass: ensure every if/for/while without { gets wrapped or has {
    expanded = []
    i = 0
    while i < len(cleaned_lines):
        line = cleaned_lines[i]
        s = line.strip()
        
        # Check if line is an if/for/while/else without {
        is_control = (
            (s.startswith("if (") or s.startswith("if(") or
             s.startswith("for (") or s.startswith("for(") or
             s.startswith("while (") or s.startswith("while(") or
             s == "else" or s.startswith("else if")) and
            not s.endswith("{") and
            not s.endswith(";")
        )
        
        if is_control and i + 1 < len(cleaned_lines):
            next_line = cleaned_lines[i + 1].strip()
            if next_line == "{":
                expanded.append(s + " {")
                i += 2
                continue
            elif not next_line.startswith("{"):
                # Single statement under if/for/while -> wrap with { ... }
                expanded.append(s + " {")
                expanded.append(next_line)
                expanded.append("}")
                i += 2
                continue
                
        expanded.append(s)
        i += 1
        
    # Third pass: indent properly
    res = []
    indent = 0
    for line in expanded:
        if not line:
            res.append("")
            continue
        if line.startswith("#"):
            res.append(line)
            continue
            
        if line.startswith("}") or line.startswith("};") or line.startswith("})"):
            indent = max(0, indent - 1)
            
        indent_str = "    " * indent
        if line in ["public:", "private:", "protected:"]:
            res.append(line)
        else:
            res.append(indent_str + line)
            
        if line.endswith("{"):
            indent += 1
            
    return "\n".join(res)

sample = """class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] ans = new int[n];
        int left = 1;
        for(int i=0;i<n;i++){ ans[i]=left; left*=nums[i]; }
        int right = 1;
        for(int i=n-1;i>=0;i--){ ans[i]*=right; right*=nums[i]; }
        return ans;
    }
}"""

print("BEFORE:")
print(sample)
print("\nAFTER:")
print(format_c_style_code(sample))
