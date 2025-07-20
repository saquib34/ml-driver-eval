from gpt_generate import generate_code
from compile_check import compile_for_architectures
from static_analysis import static_check, run_checkpatch, run_sparse
from style_checker import check_style
from scoring import score_evaluation
import re
import os

PROMPT_PATH = "basic_char_driver.txt"
GENERATED_PATH = "test_samples/generated_driver.c"
CHECKPATCH_PATH = "checkpatch.pl"

def strip_markdown_fence(code: str) -> str:
    # Remove leading/trailing triple backticks and optional language tag
    code = re.sub(r'^```[a-zA-Z]*\s*', '', code)
    code = re.sub(r'```\s*$', '', code)
    return code.strip()

with open(PROMPT_PATH) as f:
    prompt = f.read()

code = generate_code(prompt)
code = strip_markdown_fence(code)

os.makedirs(os.path.dirname(GENERATED_PATH), exist_ok=True)
with open(GENERATED_PATH, "w") as f:
    f.write(code)

compile_results = compile_for_architectures(GENERATED_PATH)
print("Compilation results by architecture:")
for arch, result in compile_results.items():
    print(f"{arch}: {result}")

# Use x86_64 result for further analysis (as an example)
compile_data = compile_results.get("x86_64", {})

static_data = static_check(GENERATED_PATH)
style_data = check_style(GENERATED_PATH)
checkpatch_data = run_checkpatch(GENERATED_PATH, CHECKPATCH_PATH)
sparse_data = run_sparse(GENERATED_PATH)

# Basic runtime/functionality test (static simulation)
def runtime_functionality_test(source_path):
    with open(source_path, 'r') as f:
        code = f.read()
    required_functions = [
        'init', 'exit', 'read', 'write'
    ]
    found = {fn: False for fn in required_functions}
    for fn in required_functions:
        # Look for function definitions like xxx_init, xxx_exit, etc.
        pattern = re.compile(r'\b\w*' + fn + r'\w*\s*\(')
        if pattern.search(code):
            found[fn] = True
    # Simulate module load/unload (cannot actually load in user space)
    can_load = compile_data.get("success", False) and found['init'] and found['exit']
    return {
        "required_functions": found,
        "can_load_module": can_load
    }

runtime_data = runtime_functionality_test(GENERATED_PATH)

final_score = score_evaluation(compile_data, style_data, static_data, checkpatch_data, sparse_data, runtime_data)
print(final_score)
