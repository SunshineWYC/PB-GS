"""Initialize a new independent website repository; never reuse a parent repository."""
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root, capture_output=True, text=True)
if result.returncode == 0:
    existing = Path(result.stdout.strip()).resolve()
    if existing != root.resolve():
        raise SystemExit('STOP: This folder is inside another repository. Copy it to an independent project_page directory first.')
    print('Repository already initialized. Its branch, history and remotes were left unchanged.')
else:
    subprocess.run(['git', 'init', '-b', 'main'], cwd=root, check=True)
    print('Initialized main. No remote, identity, credentials or GitHub repository was changed.')
