import subprocess
import sys
from pathlib import Path
import unittest


class GhostChannelCLITests(unittest.TestCase):
    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[2]
        self.python_root = self.project_root / "python"

    def test_cli_validate_assets_command_succeeds(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ghost_channel_sdk.cli",
                "validate-assets",
            ],
            cwd=self.python_root,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn('"valid": true', result.stdout.lower())

    def test_cli_sync_memory_demo_outputs_sync_result(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ghost_channel_sdk.cli",
                "sync-memory-demo",
            ],
            cwd=self.python_root,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn('"success": true', result.stdout.lower())
        self.assertIn('"changes_applied":', result.stdout.lower())

    def test_cli_workflow_demo_outputs_sync_result(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "ghost_channel_sdk.cli",
                "workflow-demo",
            ],
            cwd=self.python_root,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn('"success": true', result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
