import os
import json
import shutil
import subprocess


def get_user_input():
    repo_dir = input("Enter the repository directory (e.g., D:/Repositories): ")
    github_username = input("Enter your GitHub username: ")
    return repo_dir, github_username


def create_config_file(repo_dir, github_username):
    config = {"repo_dir": repo_dir, "github_username": github_username}
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def modify_open_repo_py(repo_dir, github_username):
    with open("open_repo.py", "r") as f:
        content = f.read()

    content = content.replace(
        'BASE_DIR = "D:/Repositories"', f'BASE_DIR = "{repo_dir}"'
    )
    content = content.replace('username = "d-eniz"', f'username = "{github_username}"')

    with open("open_repo.py", "w") as f:
        f.write(content)


def modify_repo_ahk(repo_dir):
    with open("repo.ahk", "r") as f:
        content = f.read()

    content = content.replace(
        "python D:/Repositories\\open_repo.py", f"python {repo_dir}\\open_repo.py"
    )

    with open("repo.ahk", "w") as f:
        f.write(content)


def create_directory_if_not_exists(repo_dir):
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        print(f"Created directory: {repo_dir}")
    else:
        print(f"Directory already exists: {repo_dir}")


def copy_files(repo_dir):
    shutil.copy("open_repo.py", repo_dir)
    print(f"Copied open_repo.py to {repo_dir}")

    startup_dir = os.path.join(
        os.getenv("APPDATA"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )
    shutil.copy("repo.ahk", startup_dir)
    print(f"Copied repo.ahk to {startup_dir}")


def run_ahk_script():
    startup_dir = os.path.join(
        os.getenv("APPDATA"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )

    try:
        # Use subprocess.Popen to run the AHK script in the correct directory
        subprocess.Popen(
            ["start", "repo.ahk"],
            cwd=startup_dir,
            shell=True,
        )
        print("AHK script executed successfully.")
    except Exception as e:
        print(f"Failed to run AHK script: {e}")


def main():
    repo_dir, github_username = get_user_input()
    create_directory_if_not_exists(repo_dir)
    create_config_file(repo_dir, github_username)
    modify_open_repo_py(repo_dir, github_username)
    modify_repo_ahk(repo_dir)
    copy_files(repo_dir)
    run_ahk_script()
    print("Setup completed successfully!")


if __name__ == "__main__":
    main()
