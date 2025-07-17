import subprocess

def compile_driver(source_path: str, compiler: str = "gcc") -> dict:
    result = subprocess.run(
        [compiler, "-Wall", "-Wextra", "-Werror", "-c", source_path],
        capture_output=True, text=True
    )
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "warnings": result.stderr.count("warning"),
        "errors": result.stderr.count("error")
    }

def compile_for_architectures(source_path: str) -> dict:
    """
    Compiles the source for multiple architectures and returns a dict of results.
    """
    architectures = {
        "x86_64": "gcc",
        "arm": "arm-linux-gnueabi-gcc",
        "riscv": "riscv64-linux-gnu-gcc"
    }
    results = {}
    for arch, compiler in architectures.items():
        try:
            results[arch] = compile_driver(source_path, compiler)
        except FileNotFoundError:
            results[arch] = {"success": False, "error": f"Compiler {compiler} not found."}
    return results
