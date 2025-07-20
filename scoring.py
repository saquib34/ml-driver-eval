def score_evaluation(compile_data, style_data, static_data, checkpatch_data, sparse_data, runtime_data=None) -> dict:
    score = 0
    # Compilation (Correctness)
    if compile_data.get("success"):
        score += 30
    if compile_data.get("warnings", 1) == 0:
        score += 10
    # Style (Code Quality)
    if style_data.get("long_lines", 5) < 5:
        score += 5
    if style_data.get("has_comments"):
        score += 5
    # Documentation
    if style_data.get("function_doc_count", 0) > 0:
        score += 5
    # Maintainability
    if style_data.get("avg_function_length", 100) < 50:
        score += 5
    if style_data.get("max_nesting", 10) <= 3:
        score += 5
    # Static analysis (Generic)
    if "error" not in static_data:
        score += 5
    # Security/Resource issues from static analysis
    static_issues = 0
    for issue in ["buffer overflow", "leak", "race", "input validation"]:
        if issue in static_data.lower():
            static_issues += 1
    if static_issues == 0:
        score += 10
    # Kernel style (checkpatch)
    if checkpatch_data["errors"] == 0:
        score += 10
    if checkpatch_data["warnings"] == 0:
        score += 5
    # Kernel static analysis (sparse)
    if sparse_data["errors"] == 0:
        score += 10
    if sparse_data["warnings"] == 0:
        score += 5
    # Runtime/functionality test
    if runtime_data:
        if runtime_data.get("can_load_module"):
            score += 10
        if all(runtime_data.get("required_functions", {}).values()):
            score += 10
    return {
        "compilation": compile_data,
        "style": style_data,
        "static_analysis": static_data,
        "checkpatch": checkpatch_data,
        "sparse": sparse_data,
        "runtime": runtime_data,
        "overall_score": score
    }
