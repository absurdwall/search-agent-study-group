import os
import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = REPOSITORY_ROOT / "notebooks"


class NotebookHelperTest(unittest.TestCase):
    def test_setup_adds_repository_root_to_import_path(self) -> None:
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        command = """
from pathlib import Path
import sys

import helper

repository_root = helper.setup()
assert repository_root == Path.cwd().parent.resolve()
assert sys.path[0] == str(repository_root)
"""
        result = subprocess.run(
            [sys.executable, "-c", command],
            cwd=NOTEBOOK_DIR,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
