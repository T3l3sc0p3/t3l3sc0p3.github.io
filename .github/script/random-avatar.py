import os, sys, requests, yaml, random

def get_links(token, repo_user, repo_name, branch, dirc):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/contents/{dirc}?ref={branch}"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    links = [item["download_url"] for item in response.json() if item["type"] == "file"]
    return links

def update_avatar(path, link):
    with open(path, 'r') as file:
        lines = file.readlines()
    lines[next(i for i, line in enumerate(lines) if 'avatar:' in line)] = f'avatar: "{link}"\n'
    with open(path, 'w') as file:
        file.writelines(lines)

def main(file_path):
    token = os.getenv("repo_token")
    repo_user = os.getenv("repo_user")
    repo_name = os.getenv("repo_name")
    branch = os.getenv("branch")
    dirc = os.getenv("avatar_dir")
    links = get_links(token, repo_user, repo_name, branch, dirc)
    update_avatar(file_path, random.choice(links))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <file-name>")
        sys.exit(1)
    main(sys.argv[1])
