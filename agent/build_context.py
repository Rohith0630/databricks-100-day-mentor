import os
from google import genai
from datetime import datetime

# Paths
memory_path = "../memory"
current_state_file = os.path.join(memory_path, "current_state.md")
progress_logs_path = os.path.join(memory_path, "progress_logs")

# Read current state
with open(current_state_file, "r", encoding="utf-8") as f:
    current_state = f.read()

# Read recent progress logs (sorted by filename)
progress_logs = []
if os.path.exists(progress_logs_path):
    for filename in sorted(os.listdir(progress_logs_path)):
        if filename.endswith(".md"):
            with open(os.path.join(progress_logs_path, filename), "r", encoding="utf-8") as f:
                progress_logs.append(f.read())

# --- NEW: Get today's update from you ---
print("\n--- Daily Databricks Check-in ---")
daily_update = input("What did you work on or struggle with today? \n> ")

# Combine into AI prompt
ai_prompt = f"""
Act as my Databricks Data Engineering mentor. Use the following learning state and recent progress to guide me.

# Current State
{current_state}

# Past Progress Logs
{chr(10).join(progress_logs)}

# Today's Update from Me:
{daily_update}

# Tasks for AI:
1. Acknowledge my update for today.
2. Suggest the next learning steps based on my weak areas and today's work.
3. Provide actionable guidance. No generic advice.
"""

# Initialize Gemini Client
client = genai.Client(api_key="AIzaSyB_QAwsWVhqOK3sx19_meXiubI7qZhVV8wx")

print("\nConsulting your AI mentor...")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=ai_prompt
)

# Ensure the progress_logs directory exists
os.makedirs(progress_logs_path, exist_ok=True)

# Save BOTH your input and the AI's response so it remembers tomorrow
date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
output_file = os.path.join(progress_logs_path, f"{date_str}_log.md")

log_content = f"## My Update\n{daily_update}\n\n## Mentor Feedback\n{response.text}"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(log_content)

print(f"\nConversation successfully saved to: {output_file}")


#=========================================================================================================================================

import subprocess

print("\n--- Auto-syncing to GitHub ---")
# This tells Git to look at the parent directory as the root of the repo
repo_path = ".." 

try:
    subprocess.run(f'git -C {repo_path} add .', shell=True, check=True)
    subprocess.run(f'git -C {repo_path} commit -m "Automated sync: {date_str}"', shell=True, check=True)
    subprocess.run(f'git -C {repo_path} push', shell=True, check=True)
    print("Cloud backup complete! ✅")
except subprocess.CalledProcessError:
    print("No new changes to sync or Git error encountered. ⚠️")