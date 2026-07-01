from inftastructure_git_client import GitClient
from pathlib import Path

root_dir = Path.cwd()

git_client = GitClient(
    root_dir=Path.cwd(),
    git_url='git@github.com:Mike2024New/infrastructure2.git',
    branch='main',
)

git_client.commit(commit_message_auto=True)
