def score_evaluation(compile_data, style_data, static_data, checkpatch_data, sparse_data) -> dict:
    score = 0
    # Compilation (Correctness)
    if compile_data["success"]:
        score += 30
    if compile_data["warnings"] == 0:
        score += 10
    # Style (Code Quality)
    if style_data["long_lines"] < 5:
        score += 10
    if style_data["has_comments"]:
        score += 10
    # Static analysis (Generic)
    if "error" not in static_data:
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

    return {
        "compilation": compile_data,
        "style": style_data,
        "static_analysis": static_data,
        "checkpatch": checkpatch_data,
        "sparse": sparse_data,
        "overall_score": score
    }
