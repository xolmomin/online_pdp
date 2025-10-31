import subprocess
import tempfile
import shutil
import textwrap
from pathlib import Path
import difflib

from tasks.models import Problem

DOCKER_IMAGE = "crun-python-runner"
TIMEOUT = 2.0
MEMORY = "128m"


def normalize_output(s: str):
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def run_submission(source_code: str, test_input: str):
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
            stdout, stderr = proc.communicate(test_input.rstrip() + '\n', timeout=TIMEOUT)
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


# utils/checker.py
def judge_submission(code: str, problem_id):
    code = textwrap.dedent(code)
    problem = Problem.objects.get(pk=problem_id)

    results = []

    for testcase in problem.answers_set.all():
        progress_submission = run_submission(code, testcase.input)

        # Runtime error or timeout
        if progress_submission["verdict"] != "OK":
            results.append({
                "testcase": testcase.pk,
                "verdict": "RE",  # runtime error
                "input": testcase.input,
                "expected": testcase.output,
                "actual": progress_submission.get("stdout", ""),
                "stderr": progress_submission.get("stderr", "")
            })
            break

        cmp = compare_output(progress_submission["stdout"], testcase.output)

        if cmp.get("result") == "AC":
            results.append({
                "testcase": testcase.pk,
                "verdict": "AC",
                "input": testcase.input,
                "expected": testcase.output,
                "actual": progress_submission["stdout"]
            })
        else:
            results.append({
                "testcase": testcase.pk,
                "verdict": "WA",
                "input": testcase.input,
                "expected": testcase.output,
                "actual": progress_submission["stdout"],
                "diff": cmp.get("diff", "")
            })
            break
    return results

