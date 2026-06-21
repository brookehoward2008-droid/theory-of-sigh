from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess

from scripts.codex_git_sync import CodexGitSync


class CodexGitSyncRunCommandTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sync = CodexGitSync(Path("/tmp/fake-repo"))

    @patch("subprocess.run")
    def test_run_command_returns_success_on_zero_exit(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="output", stderr="")
        success, stdout, stderr = self.sync.run_command(["git", "status"])
        self.assertTrue(success)
        self.assertEqual(stdout, "output")
        self.assertEqual(stderr, "")

    @patch("subprocess.run")
    def test_run_command_returns_failure_on_nonzero_exit(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="fatal: error")
        success, stdout, stderr = self.sync.run_command(["git", "push"])
        self.assertFalse(success)
        self.assertEqual(stderr, "fatal: error")

    @patch("subprocess.run")
    def test_run_command_handles_timeout(self, mock_run: MagicMock) -> None:
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="git", timeout=30)
        success, stdout, stderr = self.sync.run_command(["git", "pull"])
        self.assertFalse(success)
        self.assertEqual(stderr, "Command timeout")

    @patch("subprocess.run")
    def test_run_command_handles_generic_exception(self, mock_run: MagicMock) -> None:
        mock_run.side_effect = OSError("No such file")
        success, stdout, stderr = self.sync.run_command(["git", "status"])
        self.assertFalse(success)
        self.assertIn("No such file", stderr)


class CodexGitSyncStatusTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sync = CodexGitSync(Path("/tmp/fake-repo"))

    @patch("subprocess.run")
    def test_status_parses_modified_files(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="M  scripts/build.py\nMM tests/test_build.py",
            stderr="",
        )
        result = self.sync.status()
        self.assertTrue(result["valid"])
        self.assertEqual(result["modified"], ["scripts/build.py", "tests/test_build.py"])
        self.assertEqual(result["untracked"], [])
        self.assertTrue(result["has_changes"])

    @patch("subprocess.run")
    def test_status_parses_untracked_files(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="?? new_file.py\n?? docs/readme.md",
            stderr="",
        )
        result = self.sync.status()
        self.assertTrue(result["valid"])
        self.assertEqual(result["modified"], [])
        self.assertEqual(result["untracked"], ["new_file.py", "docs/readme.md"])
        self.assertTrue(result["has_changes"])

    @patch("subprocess.run")
    def test_status_reports_no_changes_on_clean_repo(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        result = self.sync.status()
        self.assertTrue(result["valid"])
        self.assertFalse(result["has_changes"])

    @patch("subprocess.run")
    def test_status_returns_invalid_on_failure(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=128, stdout="", stderr="not a git repository")
        result = self.sync.status()
        self.assertFalse(result["valid"])
        self.assertIn("not a git repository", result["error"])


class CodexGitSyncPullPushTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sync = CodexGitSync(Path("/tmp/fake-repo"))

    @patch("subprocess.run")
    def test_pull_returns_success(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="Already up to date.", stderr="")
        result = self.sync.pull()
        self.assertTrue(result["success"])
        self.assertIn("Already up to date", result["message"])

    @patch("subprocess.run")
    def test_pull_returns_error_on_failure(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="merge conflict")
        result = self.sync.pull()
        self.assertFalse(result["success"])
        self.assertIn("merge conflict", result["error"])

    @patch("subprocess.run")
    def test_push_returns_success(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="Everything up-to-date", stderr="")
        result = self.sync.push()
        self.assertTrue(result["success"])

    @patch("subprocess.run")
    def test_push_returns_error_on_failure(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="rejected")
        result = self.sync.push()
        self.assertFalse(result["success"])
        self.assertIn("rejected", result["error"])


class CodexGitSyncCommitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sync = CodexGitSync(Path("/tmp/fake-repo"))

    @patch("subprocess.run")
    def test_commit_returns_success(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="[main abc1234] my msg", stderr="")
        result = self.sync.commit("my msg")
        self.assertTrue(result["success"])

    @patch("subprocess.run")
    def test_commit_detects_nothing_to_commit(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="nothing to commit", stderr="")
        result = self.sync.commit("my msg")
        self.assertTrue(result["success"])
        self.assertTrue(result.get("skipped"))

    @patch("subprocess.run")
    def test_commit_returns_error(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="permission denied")
        result = self.sync.commit("my msg")
        self.assertFalse(result["success"])


class CodexGitSyncLogTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sync = CodexGitSync(Path("/tmp/fake-repo"))

    @patch("subprocess.run")
    def test_log_returns_commit_list(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="abc1234 first commit\ndef5678 second commit",
            stderr="",
        )
        result = self.sync.log(count=2)
        self.assertTrue(result["success"])
        self.assertEqual(len(result["commits"]), 2)
        self.assertIn("abc1234 first commit", result["commits"][0])

    @patch("subprocess.run")
    def test_log_returns_empty_list_on_no_output(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        result = self.sync.log()
        self.assertTrue(result["success"])
        self.assertEqual(result["commits"], [])


class CodexGitSyncAddAllTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sync = CodexGitSync(Path("/tmp/fake-repo"))

    @patch("subprocess.run")
    def test_add_all_returns_success(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        result = self.sync.add_all()
        self.assertTrue(result["success"])

    @patch("subprocess.run")
    def test_add_all_returns_error(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="permission denied")
        result = self.sync.add_all()
        self.assertFalse(result["success"])


class CodexGitSyncAutoSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sync = CodexGitSync(Path("/tmp/fake-repo"))

    @patch("subprocess.run")
    def test_auto_sync_fails_if_pull_fails(self, mock_run: MagicMock) -> None:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="network error")
        result = self.sync.auto_sync()
        self.assertFalse(result["success"])
        self.assertIn("Pull failed", result["error"])

    @patch("subprocess.run")
    def test_auto_sync_succeeds_with_no_changes(self, mock_run: MagicMock) -> None:
        def side_effect(cmd, **kwargs):
            if "pull" in cmd:
                return MagicMock(returncode=0, stdout="Already up to date.", stderr="")
            if "--porcelain" in cmd:
                return MagicMock(returncode=0, stdout="", stderr="")
            return MagicMock(returncode=0, stdout="", stderr="")

        mock_run.side_effect = side_effect
        result = self.sync.auto_sync()
        self.assertTrue(result["success"])
        self.assertIn("No changes", result["message"])


if __name__ == "__main__":
    unittest.main()
