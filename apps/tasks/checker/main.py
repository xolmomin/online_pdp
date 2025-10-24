import subprocess
import tempfile
import shutil
from pathlib import Path
import difflib

DOCKER_IMAGE = "crun-python-runner"
TIMEOUT = 2.0
MEMORY = "128m"


def normalize_output(s: str):
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def run_in_docker(source_code: str, test_input: str):
    tmp = Path(tempfile.mkdtemp(prefix="crun-judge-"))
    try:
        workspace = tmp / "workspace"
        workspace.mkdir()
        code_file = workspace / "main.py"
        code_file.write_text(source_code)

        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "--memory", MEMORY,
            "--cpus", "0.5",
            "--pids-limit", "64",
            "--read-only",
            "--tmpfs", "/tmp:rw,size=32m",
            "--tmpfs", "/var:rw,size=16m",
            "--tmpfs", "/root:rw,size=16m",
            "--device", "/dev/null:/dev/null",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "-v", f"{workspace}:/home/runner/workspace:ro",
            "-w", "/home/runner/workspace",
            "-i", DOCKER_IMAGE,
        ]

        proc = subprocess.Popen(
            docker_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            stdout, stderr = proc.communicate(test_input, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            proc.kill()
            return {"verdict": "TLE", "stdout": "", "stderr": "timeout (wall-clock)"}

        exit_code = proc.returncode
        if exit_code != 0 and stderr:
            return {"verdict": "RE", "stdout": stdout, "stderr": stderr}

        return {"verdict": "OK", "stdout": stdout, "stderr": stderr}

    finally:
        shutil.rmtree(tmp)


def compare_output(user_out: str, expected_out: str):
    u = normalize_output(user_out)
    e = normalize_output(expected_out)
    if u == e:
        return {"result": "AC"}
    else:
        diff = "\n".join(difflib.unified_diff(e.splitlines(), u.splitlines(), lineterm=""))
        return {"result": "WA", "diff": diff}


def judge_submission(source_code: str, test_cases: list[dict]):
    """
    Run and evaluate code against multiple test cases.

    Args:
        source_code (str): The Python code the user submitted.
        test_cases (list[dict]): Each dict must have {'input': str, 'expected': str}.

    Returns:
        dict: Overall verdict and detailed per-test results.
    """
    results = []
    all_passed = True

    for i, case in enumerate(test_cases, start=1):
        runr = run_in_docker(source_code, case["input"])

        if runr["verdict"] != "OK":
            results.append({
                "test": i,
                "verdict": runr["verdict"],
                "stdout": runr["stdout"],
                "stderr": runr["stderr"],
            })
            all_passed = False
            continue

        cmp = compare_output(runr["stdout"], case["expected"])
        verdict = cmp.get("result")

        results.append({
            "test": i,
            "verdict": verdict,
            "stdout": runr["stdout"],
            "stderr": runr["stderr"],
            "diff": cmp.get("diff", "")
        })

        if verdict != "AC":
            all_passed = False

    return {
        "final_verdict": "✅ Accepted" if all_passed else "❌ Wrong Answer",
        "results": results
    }
