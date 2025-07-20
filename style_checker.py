import re

def check_style(source_path: str) -> dict:
    with open(source_path, 'r') as f:
        code = f.read()
    lines = code.splitlines()
    long_lines = sum(1 for line in lines if len(line) > 80)
    has_comments = "//" in code or "/*" in code

    # Check for function-level documentation (simple heuristic: comment before function)
    function_doc_count = 0
    function_pattern = re.compile(r'^\s*\w[\w\s\*]+\([^)]*\)\s*\{')
    for i, line in enumerate(lines):
        if function_pattern.match(line):
            if i > 0 and (lines[i-1].strip().startswith('//') or lines[i-1].strip().startswith('/*')):
                function_doc_count += 1

    # Maintainability: function length and nesting depth
    function_lengths = []
    max_nesting = 0
    current_length = 0
    nesting_stack = []
    in_function = False
    for line in lines:
        if '{' in line:
            nesting_stack.append('{')
            if not in_function:
                in_function = True
                current_length = 1
            else:
                current_length += 1
        elif '}' in line and nesting_stack:
            nesting_stack.pop()
            current_length += 1
            if not nesting_stack:
                in_function = False
                function_lengths.append(current_length)
                current_length = 0
        elif in_function:
            current_length += 1
        # Track max nesting
        max_nesting = max(max_nesting, len(nesting_stack))

    avg_function_length = sum(function_lengths) / len(function_lengths) if function_lengths else 0

    return {
        "long_lines": long_lines,
        "has_comments": has_comments,
        "function_doc_count": function_doc_count,
        "avg_function_length": avg_function_length,
        "max_nesting": max_nesting
    }
