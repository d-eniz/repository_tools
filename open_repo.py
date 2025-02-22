import os

BASE_DIR = "D:/test"
username = "d-eniz"


def get_repo_name():
    return input("Enter the repository name: ")


def open_repo(repo_path):
    os.chdir(repo_path)
    os.system("code .")
    os.system("taskkill /f /im cmd.exe")


def clone_repo(repo_name, repo_path):
    os.system(f'git clone git@github.com:{username}/{repo_name}.git "{repo_path}"')
    open_repo(repo_path)


def check_github_repo(repo_name):
    result = os.system(f"git ls-remote git@github.com:{username}/{repo_name}.git")
    return result == 0


def create_new_repo_on_github(repo_name):
    os.system(f"gh repo create {username}/{repo_name} --private")


def initialize_local_repo(repo_path, repo_name):
    os.chdir(repo_path)
    os.system("git init")
    os.system(f"git remote add origin git@github.com:{username}/{repo_name}.git")

    with open("README.md", "w") as f:
        f.write(f"# {repo_name}")

    os.system("git add README.md")
    os.system('git commit -m "Initial commit"')
    os.system("git branch -M main")
    os.system("git push -u origin main")


while True:
    repo_name = get_repo_name()
    repo_path = os.path.join(BASE_DIR, repo_name)

    if os.path.exists(repo_path):
        open_repo(repo_path)
        break
    elif check_github_repo(repo_name):
        clone_repo(repo_name, repo_path)
        break
    else:
        print(f"Repository '{repo_name}' does not exist locally or on GitHub.")
        create_new = input(
            "\nDo you want to create a new repository on GitHub? (y/n): "
        ).lower()
        if create_new == "y":
            create_new_repo_on_github(repo_name)
            os.makedirs(repo_path)
            initialize_local_repo(repo_path, repo_name)
            open_repo(repo_path)
            break
        else:
            print("Please try again.\n")
