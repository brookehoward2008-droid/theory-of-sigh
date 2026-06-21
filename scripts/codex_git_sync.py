#!/usr/bin/env python3
"""
Codex Git Sync: Automated push, pull, and commit for Codex workflows.

Enables automatic GitHub synchronization for publication automation.

Usage:
    python codex_git_sync.py                    # Auto sync (pull → commit → push)
    python codex_git_sync.py --pull             # Pull from origin
    python codex_git_sync.py --push             # Push to origin
    python codex_git_sync.py --commit "message" # Commit with message
    python codex_git_sync.py --status           # Check git status
    python codex_git_sync.py --log              # Show recent commits
"""

from __future__ import annotations

import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from datetime import datetime


class CodexGitSync:
    """Automated Git operations for Codex workflows."""

    def __init__(self, repo_path: Path):
        """Initialize with repository path."""
        self.repo_path = Path(repo_path)
        self.remote = "origin"
        self.branch = "main"

    def run_command(self, cmd: list[str]) -> tuple[bool, str, str]:
        """Run git command and return status, stdout, stderr."""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", "Command timeout"
        except FileNotFoundError as e:
            return False, "", f"Command not found: {e}"
        except OSError as e:
            return False, "", f"OS error running command: {e}"

    def status(self) -> dict:
        """Check git status."""
        success, stdout, stderr = self.run_command(["git", "status", "--porcelain"])
        
        if not success:
            return {"valid": False, "error": stderr}
        
        modified = []
        untracked = []
        
        for line in stdout.split("\n"):
            if not line:
                continue
            status_code = line[:2]
            filename = line[3:]
            
            if status_code in ["M ", "MM"]:
                modified.append(filename)
            elif status_code == "??":
                untracked.append(filename)
        
        return {
            "valid": True,
            "modified": modified,
            "untracked": untracked,
            "has_changes": len(modified) > 0 or len(untracked) > 0
        }

    def pull(self) -> dict:
        """Pull from origin."""
        print(f"[GIT] Pulling from {self.remote}/{self.branch}...")
        success, stdout, stderr = self.run_command(
            ["git", "pull", self.remote, self.branch]
        )
        
        if success:
            print(f"[OK] Pull successful")
            return {"success": True, "message": stdout}
        else:
            print(f"[ERROR] Pull failed: {stderr}")
            return {"success": False, "error": stderr}

    def add_all(self) -> dict:
        """Stage all changes."""
        print("[GIT] Staging changes...")
        success, stdout, stderr = self.run_command(["git", "add", "-A"])
        
        if success:
            print("[OK] Changes staged")
            return {"success": True}
        else:
            print(f"[ERROR] Stage failed: {stderr}")
            return {"success": False, "error": stderr}

    def commit(self, message: str) -> dict:
        """Commit changes."""
        print(f"[GIT] Committing: {message}")
        
        cmd = [
            "git", "commit", "-m", message,
            "--trailer", "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
        ]
        
        success, stdout, stderr = self.run_command(cmd)
        
        if success:
            print(f"[OK] Commit successful")
            return {"success": True, "message": stdout}
        else:
            # Check if there are no changes to commit
            if "nothing to commit" in stderr.lower() or "nothing to commit" in stdout.lower():
                print("[SKIP] No changes to commit")
                return {"success": True, "skipped": True}
            print(f"[ERROR] Commit failed: {stderr}")
            return {"success": False, "error": stderr}

    def push(self) -> dict:
        """Push to origin."""
        print(f"[GIT] Pushing to {self.remote}/{self.branch}...")
        success, stdout, stderr = self.run_command(
            ["git", "push", self.remote, self.branch]
        )
        
        if success:
            print(f"[OK] Push successful")
            return {"success": True, "message": stdout}
        else:
            print(f"[ERROR] Push failed: {stderr}")
            return {"success": False, "error": stderr}

    def log(self, count: int = 5) -> dict:
        """Show recent commits."""
        success, stdout, stderr = self.run_command(
            ["git", "log", f"-{count}", "--oneline"]
        )
        
        if success:
            return {
                "success": True,
                "commits": stdout.split("\n") if stdout else []
            }
        else:
            return {"success": False, "error": stderr}

    def auto_sync(self) -> dict:
        """Auto sync: pull → commit → push."""
        print("\n" + "="*60)
        print("CODEX AUTO GIT SYNC")
        print("="*60 + "\n")
        
        # Step 1: Pull
        pull_result = self.pull()
        if not pull_result["success"]:
            return {"success": False, "error": "Pull failed", "details": pull_result}
        
        # Step 2: Check status
        status_result = self.status()
        if not status_result["valid"]:
            return {"success": False, "error": "Status check failed"}
        
        if not status_result["has_changes"]:
            print("[SKIP] No changes to sync\n")
            return {"success": True, "message": "No changes"}
        
        print(f"[INFO] Found {len(status_result['modified'])} modified files")
        print(f"[INFO] Found {len(status_result['untracked'])} untracked files\n")
        
        # Step 3: Stage
        add_result = self.add_all()
        if not add_result["success"]:
            return {"success": False, "error": "Stage failed"}
        
        # Step 4: Commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"chore: Codex auto-sync {timestamp}"
        
        commit_result = self.commit(commit_message)
        if not commit_result["success"]:
            return {"success": False, "error": "Commit failed"}
        
        if commit_result.get("skipped"):
            print("[SKIP] No changes to commit\n")
            return {"success": True, "message": "No changes to commit"}
        
        # Step 5: Push
        push_result = self.push()
        if not push_result["success"]:
            return {"success": False, "error": "Push failed"}
        
        print("\n" + "="*60)
        print("✓ AUTO SYNC COMPLETE")
        print("="*60 + "\n")
        
        return {"success": True, "message": "Sync complete"}


def main():
    """Main entry point."""
    parser = ArgumentParser(description="Codex Git Sync - Auto push, pull, commit")
    parser.add_argument(
        "--pull",
        action="store_true",
        help="Pull from origin"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push to origin"
    )
    parser.add_argument(
        "--commit",
        type=str,
        help="Commit with custom message"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show git status"
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="Show recent commits"
    )
    
    args = parser.parse_args()
    
    # Detect repo root
    repo_path = Path(__file__).resolve().parents[1]
    sync = CodexGitSync(repo_path)
    
    try:
        result = {"success": True}
        
        if args.status:
            status = sync.status()
            print(f"\nModified: {status.get('modified', [])}")
            print(f"Untracked: {status.get('untracked', [])}\n")
        elif args.log:
            log_result = sync.log()
            if log_result["success"]:
                print("\nRecent commits:")
                for commit in log_result["commits"]:
                    print(f"  {commit}")
                print()
            result = log_result
        elif args.pull:
            result = sync.pull()
        elif args.push:
            result = sync.push()
        elif args.commit:
            result = sync.commit(args.commit)
        else:
            # Default: auto sync
            result = sync.auto_sync()
        
        return 0 if result.get("success", False) else 1
    
    except KeyboardInterrupt:
        print("\n[CANCEL] Sync cancelled by user")
        return 130
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
