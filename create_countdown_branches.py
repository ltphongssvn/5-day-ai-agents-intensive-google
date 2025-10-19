#!/usr/bin/env python3
# File: ~/code/ltphongssvn/5-day-ai-agents-intensive-google/create_countdown_branches.py
"""
Automated branch creation script for countdown to course kickoff.
Creates sequential branches with decreasing day counts.
"""

import subprocess
from datetime import datetime


def run_git_command(command):
    """Execute git command and return output."""
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, check=False
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def get_current_branch():
    """Get current git branch name."""
    returncode, stdout, stderr = run_git_command("git branch --show-current")
    if returncode != 0:
        raise RuntimeError(f"Failed to get current branch: {stderr}")
    return stdout


def calculate_days_to_kickoff():
    """Calculate days remaining until November 10, 2025."""
    kickoff_date = datetime(2025, 11, 10)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    days_remaining = (kickoff_date - today).days
    return days_remaining


def create_countdown_branch(days_count, previous_branch):
    """Create new countdown branch from previous branch."""
    branch_name = f"feature/phong-agents-{days_count}-days-to-kickoff-on-Monday-November-10-Friday-November-14"

    print(f"\n{'='*80}")
    print(f"Creating branch: {branch_name}")
    print(f"From: {previous_branch}")
    print(f"{'='*80}")

    # Switch to previous branch
    print(f"\n1. Switching to {previous_branch}...")
    returncode, stdout, stderr = run_git_command(f"git checkout {previous_branch}")
    if returncode != 0:
        print(f"   ❌ Error: {stderr}")
        return False, previous_branch
    print(f"   ✓ Switched to {previous_branch}")

    # Create and switch to new branch
    print(f"\n2. Creating new branch: {branch_name}...")
    returncode, stdout, stderr = run_git_command(f"git checkout -b {branch_name}")
    if returncode != 0:
        print(f"   ❌ Error: {stderr}")
        return False, previous_branch
    print(f"   ✓ Created and switched to {branch_name}")

    return True, branch_name


def main():
    """Main execution function."""
    print("\n" + "=" * 80)
    print("COUNTDOWN BRANCH CREATION SCRIPT")
    print("=" * 80)

    # Verify we're in a git repository
    returncode, stdout, stderr = run_git_command("git rev-parse --git-dir")
    if returncode != 0:
        print("\n❌ Error: Not a git repository")
        return

    # Get starting branch
    try:
        starting_branch = get_current_branch()
        print(f"\nStarting branch: {starting_branch}")
    except RuntimeError as e:
        print(f"\n❌ {e}")
        return

    # Calculate days to kickoff
    days_remaining = calculate_days_to_kickoff()
    print(f"Days to kickoff: {days_remaining}")

    if days_remaining <= 0:
        print("\n⚠️  Kickoff date has passed!")
        return

    # Confirm before proceeding
    print(f"\nThis will create {days_remaining} branches")
    response = input("Continue? (y/n): ").strip().lower()
    if response != "y":
        print("\n❌ Aborted by user")
        return

    # Create branches - start with current day (22) and work down to 1
    previous_branch = starting_branch
    created_count = 0
    today_branch = None

    for day in range(days_remaining, 0, -1):
        success, current_branch = create_countdown_branch(day, previous_branch)
        if success:
            created_count += 1
            previous_branch = current_branch
            # Mark the branch matching today's countdown
            if day == days_remaining:
                today_branch = current_branch
        else:
            print(f"\n❌ Failed to create branch for day {day}")
            break

    # Switch to today's branch after all branches created
    if today_branch:
        print(f"\n{'='*80}")
        print(f"Switching to today's branch: {today_branch}")
        print(f"{'='*80}")
        returncode, stdout, stderr = run_git_command(f"git checkout {today_branch}")
        if returncode == 0:
            print(f"✓ Now on {today_branch}")
        else:
            print(f"❌ Failed to switch: {stderr}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✓ Created {created_count} branches")
    print(f"✓ Current branch: {today_branch if today_branch else previous_branch}")
    print(f"✓ Today is day {days_remaining} to kickoff")
    print("\nTo push all branches to remote, run:")
    print("  git push origin --all")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
