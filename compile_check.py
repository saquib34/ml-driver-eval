import subprocess

def compile_driver(source_path: str) -> dict:
    result = subprocess.run(
        ["gcc", "-Wall", "-Wextra", "-Werror", "-c", source_path],
        capture_output=True, text=True
    )
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "warnings": result.stderr.count("warning"),
        "errors": result.stderr.count("error")
    }
