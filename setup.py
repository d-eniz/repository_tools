import os
import json
import shutil
import subprocess
import tempfile


def get_user_input():
    repo_dir = input("Enter the repository directory (e.g., D:/Repositories): ")
    github_username = input("Enter your GitHub username: ")
    return repo_dir, github_username


def load_or_create_config():
    if os.path.exists("config.json"):
        print("\nLoading configuration from config.json")
        print("Edit or delete config.json to change the configuration.\n")
        with open("config.json", "r") as f:
            config = json.load(f)
        return config["repo_dir"], config["github_username"]
    else:
        repo_dir, github_username = get_user_input()
        config = {"repo_dir": repo_dir, "github_username": github_username}
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
        return repo_dir, github_username


def modify_file_content(content, repo_dir, github_username):
    content = content.replace(
        'BASE_DIR = "BASE_DIR"', f'BASE_DIR = "{repo_dir}"'
    )
    content = content.replace('username = "username"', f'username = "{github_username}"')
    return content


def modify_ahk_script_content(content, repo_dir):
    content = content.replace(
        "python path\\to\\repo\\open_repo.py", f"python {repo_dir}\\open_repo.py"
    )
    return content


def create_temp_file_with_modifications(original_file, repo_dir, github_username=None):
    with open(original_file, "r") as f:
        content = f.read()

    if original_file.endswith(".py"):
        modified_content = modify_file_content(content, repo_dir, github_username)
    elif original_file.endswith(".ahk"):
        modified_content = modify_ahk_script_content(content, repo_dir)
    else:
        raise ValueError("Unsupported file type for modification.")

    temp_file = tempfile.NamedTemporaryFile(
        delete=False, mode="w", suffix=os.path.splitext(original_file)[1]
    )
    temp_file.write(modified_content)
    temp_file.close()

    return temp_file.name


def create_directory_if_not_exists(repo_dir):
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)
        print(f"Created directory: {repo_dir}")
    else:
        print(f"Directory already exists: {repo_dir}")


def copy_files(repo_dir, temp_open_repo_py, temp_repo_ahk):
    shutil.copy(temp_open_repo_py, os.path.join(repo_dir, "open_repo.py"))
    print(f"Copied open_repo.py to {repo_dir}")

    startup_dir = os.path.join(
        os.getenv("APPDATA"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )
    shutil.copy(temp_repo_ahk, os.path.join(startup_dir, "repo.ahk"))
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
        subprocess.Popen(
            ["start", "repo.ahk"],
            cwd=startup_dir,
            shell=True,
        )
        print("AHK script executed successfully.")
    except Exception as e:
        print(f"Failed to run AHK script: {e}")


def main():
    repo_dir, github_username = load_or_create_config()
    create_directory_if_not_exists(repo_dir)

    temp_open_repo_py = create_temp_file_with_modifications(
        "open_repo.py", repo_dir, github_username
    )
    temp_repo_ahk = create_temp_file_with_modifications("repo.ahk", repo_dir)

    copy_files(repo_dir, temp_open_repo_py, temp_repo_ahk)

    run_ahk_script()

    os.unlink(temp_open_repo_py)
    os.unlink(temp_repo_ahk)
    print("Setup completed successfully!")


if __name__ == "__main__":
    main()
