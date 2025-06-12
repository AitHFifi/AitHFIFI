import os
import re
import requests
from github import Github

# Authenticate with GitHub
g = Github(os.environ.get("GH_TOKEN"))
user = g.get_user("AitHFifi")  # Your GitHub username

# Get repos sorted by updated time
repos = sorted(user.get_repos(), key=lambda repo: repo.updated_at, reverse=True)

# Generate markdown for the latest 5 projects
project_md = ""
count = 0
for repo in repos:
    if not repo.fork and not repo.private:  # Only show original, public repos
        project_md += f"- [{repo.name}]({repo.html_url}) - {repo.description or 'No description'}\n"
        count += 1
        if count >= 5:
            break

# Read the README file
with open("README.md", "r") as f:
    readme = f.read()

# Replace the project section
pattern = r"<!-- LATEST-PROJECTS:START -->[\s\S]*?<!-- LATEST-PROJECTS:END -->"
replacement = f"<!-- LATEST-PROJECTS:START -->\n{project_md}<!-- LATEST-PROJECTS:END -->"
new_readme = re.sub(pattern, replacement, readme)

# Write the updated README
with open("README.md", "w") as f:
    f.write(new_readme)
