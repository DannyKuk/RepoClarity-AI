from app.repo.scanner import scan_repository

repo_path = "../"  # point this to a real repo

files = scan_repository(repo_path)

print(f"Found {len(files)} files")

for f in files[:5]:
    print(f["path"])