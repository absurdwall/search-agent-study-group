import importlib.util
import tempfile
import unittest
from pathlib import Path


ENV_MODULE = (
    Path(__file__).resolve().parents[1]
    / "notebooks"
    / "mcp_workshop"
    / "env.py"
)


def load_env_module():
    spec = importlib.util.spec_from_file_location("workshop_env", ENV_MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkshopEnvDiscoveryTests(unittest.TestCase):
    def test_prefers_env_beside_notebooks(self):
        module = load_env_module()
        with tempfile.TemporaryDirectory() as temporary_directory:
            week_root = Path(temporary_directory) / "weeks" / "2026-08-11"
            notebook_root = week_root / "notebooks"
            notebook_root.mkdir(parents=True)
            notebook_env = notebook_root / ".env"
            week_env = week_root / ".env"
            notebook_env.touch()
            week_env.touch()

            candidates = module.env_file_candidates(
                repository_root=week_root,
                cwd=notebook_root,
                home=Path(temporary_directory) / "home",
            )

            self.assertEqual(candidates[0], notebook_env)
            self.assertLess(candidates.index(notebook_env), candidates.index(week_env))

    def test_finds_notebook_env_when_kernel_starts_elsewhere(self):
        module = load_env_module()
        with tempfile.TemporaryDirectory() as temporary_directory:
            week_root = Path(temporary_directory) / "weeks" / "2026-08-11"
            notebook_root = week_root / "notebooks"
            unrelated_cwd = Path(temporary_directory) / "jupyter-runtime"
            notebook_root.mkdir(parents=True)
            unrelated_cwd.mkdir()
            notebook_env = notebook_root / ".env"
            notebook_env.touch()

            candidates = module.env_file_candidates(
                repository_root=week_root,
                cwd=unrelated_cwd,
                home=Path(temporary_directory) / "home",
            )

            self.assertIn(notebook_env, candidates)


if __name__ == "__main__":
    unittest.main()
