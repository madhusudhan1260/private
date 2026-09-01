import os
import random
import subprocess
from datetime import datetime, timedelta

def get_repo_path(prompt, default="."):
    while True:
        user_input = input(f"{prompt} (default current directory): ")
        if not user_input.strip():
            return default
        if os.path.isdir(user_input):
            return user_input
        else:
            print("Directory does not exist. Please enter a valid path.")

def get_filename(prompt, default="data.txt"):
    user_input = input(f"{prompt} (default {default}): ")
    if not user_input.strip():
        return default
    return user_input

def get_int_range(prompt, default_min=1, default_max=15):
    print(f"{prompt} [Press Enter for default {default_min}-{default_max}]")
    min_val = input(f"Min commits per day (default {default_min}): ").strip()
    max_val = input(f"Max commits per day (default {default_max}): ").strip()
    
    min_val = int(min_val) if min_val.isdigit() and int(min_val) > 0 else default_min
    max_val = int(max_val) if max_val.isdigit() and int(max_val) >= min_val else default_max
    return min_val, max_val

def make_commit(date, repo_path, filename, message="graph-greener!"):
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")
    
    subprocess.run(["git", "add", filename], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    subprocess.run(
        ["git", "commit", "-m", message], 
        cwd=repo_path, 
        env=env, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )

def main():
    print("=" * 60)
    print("🌱 GitHub Contribution Graph Filler 🌱")
    print("=" * 60)

    repo_path = get_repo_path("Enter the path to your local git repository", ".")
    filename = get_filename("Enter the filename to modify for commits", "data.txt")
    min_commits, max_commits = get_int_range("Set daily commit range (min-max):", 1, 15)

    today = datetime.now()
    total_days = 800
    print(f"\nGenerating commits for the past {total_days} days...")

    total_commits = 0
    for day_offset in range(total_days, -1, -1):
        target_day = today - timedelta(days=day_offset)
        daily_count = random.randint(min_commits, max_commits)
        
        for _ in range(daily_count):
            random_seconds = random.randint(0, 86399)
            commit_time = target_day.replace(hour=0, minute=0, second=0) + timedelta(seconds=random_seconds)
            make_commit(commit_time, repo_path, filename)
            total_commits += 1

        print(f"[{365 - day_offset + 1}/366] {target_day.strftime('%Y-%m-%d')}: {daily_count} commits", end="\r")

    print(f"\n\nTotal commits created: {total_commits}")
    print("Pushing commits to remote repository...")
    subprocess.run(["git", "push"], cwd=repo_path)
    print("✅ Complete! GitHub may take a few minutes to recalculate your contribution graph.")

if __name__ == "__main__":
    main()