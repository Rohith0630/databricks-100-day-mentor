import os

# Paths
memory_path = "../memory"  # adjust if running from agent folder
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

# Combine into AI prompt
ai_prompt = f"""
Act as my Databricks Data Engineering mentor. Use the following learning state and recent progress to guide me:

# Current State
{current_state}

# Recent Progress Logs
{chr(10).join(progress_logs)}

# Tasks for AI:
1. Suggest the next learning steps based on my weak areas.
2. Recommend practical exercises to solidify concepts.
3. Identify any missing topics I should cover before becoming job-ready.

Provide actionable guidance. No generic advice.
"""

# Save to a file
output_file = os.path.join(memory_path, "ai_prompt.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(ai_prompt)

print(f"AI context prompt generated: {output_file}")
