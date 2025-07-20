import subprocess

def static_check(source_path: str) -> str:
    result = subprocess.run(["cppcheck", source_path], capture_output=True, text=True)
    return result.stderr

def run_checkpatch(source_path: str, checkpatch_path: str = "checkpatch.pl") -> dict:
   
    result = subprocess.run(
        ["perl", checkpatch_path, "--no-tree", "--file", source_path],
        capture_output=True, text=True
    )
    output = result.stdout
    warnings = output.count("WARNING:")
    errors = output.count("ERROR:")
    return {
        "raw_output": output,
        "warnings": warnings,
        "errors": errors
    }

def run_sparse(source_path: str) -> dict:

    result = subprocess.run(
        ["sparse", source_path],
        capture_output=True, text=True
    )
    output = result.stderr + result.stdout
    warnings = output.lower().count("warning:")
    errors = output.lower().count("error:")
    return {
        "raw_output": output,
        "warnings": warnings,
        "errors": errors
    }
