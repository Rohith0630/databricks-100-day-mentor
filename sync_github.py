import os
import subprocess

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(result.stderr)
        exit(1)
    else:
        print(result.stdout)

def git_sync():
    print("Adding all changes...")
    run("git add .")
    print("Committing...")
    run('git commit -m "Automated sync: update progress logs and state"')
    print("Pushing to GitHub...")
    run("git push")

if __name__ == "__main__":
    git_sync()