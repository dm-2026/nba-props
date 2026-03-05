"""
deploy.py — Push today's NBA props report to GitHub Pages.
Run this after nba_props_fetch.py generates the HTML.

Your site: https://dm-2026.github.io/nba-props
"""

import os
import sys
import glob
import shutil
import subprocess
from datetime import datetime

GITHUB_REPO = "dm-2026/nba-props"
REPO_URL = "https://github.com/dm-2026/nba-props.git"

def run(cmd, check=True):
    print(f"  > {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                            cwd=os.path.dirname(os.path.abspath(__file__)))
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        if check:
            sys.exit(1)
    return result

def ensure_git():
    """Make sure git is initialized and connected to GitHub."""
    folder = os.path.dirname(os.path.abspath(__file__))
    git_dir = os.path.join(folder, ".git")
    if not os.path.exists(git_dir):
        print("  Git not initialized — setting up...")
        run("git init")
        run(f"git remote add origin {REPO_URL}")
        run("git fetch origin")
        run("git checkout -b main origin/main", check=False)
        print("  Git ready.")
    else:
        # Make sure remote exists
        result = run("git remote get-url origin", check=False)
        if result.returncode != 0:
            run(f"git remote add origin {REPO_URL}")

def deploy():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ensure_git()

    # Find today's generated HTML
    today = datetime.now().strftime("%m%d")
    html_files = glob.glob(f"nba_props_{today}.html") or glob.glob("nba_props_*.html")

    if not html_files:
        print("ERROR: No HTML report found. Run nba_props_fetch.py first.")
        sys.exit(1)

    src = sorted(html_files)[-1]
    print(f"\nDeploying {src} -> https://dm-2026.github.io/nba-props")

    shutil.copy(src, "index.html")
    print(f"  Copied {src} -> index.html")

    run("git add index.html")
    run(f'git commit -m "NBA props {datetime.now().strftime("%Y-%m-%d %H:%M")}"')
    run("git push origin main")

    print(f"\n[DONE] Live at: https://dm-2026.github.io/nba-props")
    print("Share that link with your friends!")

if __name__ == "__main__":
    deploy()
