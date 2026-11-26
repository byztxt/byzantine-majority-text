"""Regeneration determinism, checked in a throwaway git worktree at HEAD.

The tests never write to the developer's working tree. Each class creates a
detached worktree of the committed HEAD, runs the real generator scripts there,
and asserts that (a) two runs are byte-identical and (b) the committed outputs
already match a fresh run. Skips loudly when `git worktree` is unavailable.
"""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATORS = [
    ["byz.build"],
    ["byz.diff"],
    ["byz.contract"],
    ["byz.reconcile"],
    ["byz.verify"],
]
SKIP_MESSAGE = (
    "`git worktree` is unavailable, so the hermetic regeneration checks cannot "
    "run; run them in a normal git clone with worktree support"
)


def _run(command, cwd, env=None):
    result = subprocess.run(
        command,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"{' '.join(command)} failed in {cwd}: {result.stderr[-2000:]}"
        )
    return result


def make_worktree():
    """Create a detached worktree of HEAD; return its path or None."""
    parent = Path(tempfile.mkdtemp(prefix="byz-repro-"))
    target = parent / "wt"
    result = subprocess.run(
        ["git", "-C", str(ROOT), "worktree", "add", "--detach", str(target), "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        shutil.rmtree(parent, ignore_errors=True)
        return None
    return target


def remove_worktree(path):
    if path is None:
        return
    subprocess.run(
        ["git", "-C", str(ROOT), "worktree", "remove", "--force", str(path)],
        capture_output=True,
        text=True,
    )
    shutil.rmtree(path.parent, ignore_errors=True)
    # Prune after the directory is gone so a failed `worktree remove` cannot
    # leave stale worktree metadata behind.
    subprocess.run(
        ["git", "-C", str(ROOT), "worktree", "prune"],
        capture_output=True,
        text=True,
    )


def run_generators(worktree):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(worktree / "src")
    for arguments in GENERATORS:
        command = [sys.executable, "-m", *arguments]
        _run(command, cwd=worktree, env=env)


def status(worktree):
    result = _run(
        ["git", "-C", str(worktree), "status", "--porcelain"],
        cwd=worktree,
    )
    return result.stdout.strip()


def snapshot(worktree):
    hashes = {}
    for base in (
        worktree / "editions",
        worktree / "reports" / "diffs",
        worktree / "reports" / "baseline",
        worktree / "reports" / "reconciliation",
        worktree / "docs" / "contract",
    ):
        for path in sorted(base.rglob("*")):
            if path.is_file():
                hashes[str(path.relative_to(worktree))] = hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
    for rel in (
        "docs/EDITIONS.md",
        "docs/HISTORY.md",
        "docs/DATA_CONTRACT.md",
        "docs/PROVENANCE.md",
        "data/provenance/rp2005.toml",
        "data/provenance/rp2018.toml",
        "README.md",
    ):
        path = worktree / rel
        hashes[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


class RegenerationDeterminismTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.worktree = make_worktree()
        if cls.worktree is None:
            raise unittest.SkipTest(SKIP_MESSAGE)
        try:
            if status(cls.worktree):
                raise AssertionError("fresh worktree at HEAD is not clean")
            run_generators(cls.worktree)
            cls.first = snapshot(cls.worktree)
        except BaseException:
            remove_worktree(cls.worktree)
            raise

    @classmethod
    def tearDownClass(cls):
        remove_worktree(cls.worktree)

    def test_committed_outputs_match_a_fresh_run(self):
        self.assertEqual(
            status(self.worktree),
            "",
            "generated outputs differ from the committed HEAD",
        )

    def test_two_runs_are_byte_identical(self):
        run_generators(self.worktree)
        second = snapshot(self.worktree)
        changed = sorted(
            path
            for path in set(self.first) | set(second)
            if self.first.get(path) != second.get(path)
        )
        self.assertEqual(changed, [], "regeneration is not deterministic")
        staging = [
            path.name
            for path in (self.worktree / "editions").iterdir()
            if path.name.startswith(".")
        ]
        self.assertEqual(staging, [], "recovery left a staging directory behind")


if __name__ == "__main__":
    unittest.main()
