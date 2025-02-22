# Run this script to remove the AHK script, Python script, and config file from the system

import os
import json


def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
        return config
    else:
        print("config.json does not exist. Nothing to remove.")
        return None


def remove_ahk_script():
    startup_dir = os.path.join(
        os.getenv("APPDATA"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )
    ahk_script_path = os.path.join(startup_dir, "repo.ahk")

    if os.path.exists(ahk_script_path):
        os.remove(ahk_script_path)
        print(f"Removed AHK script from startup directory: {ahk_script_path}")
    else:
        print("AHK script does not exist in the startup directory.")


def remove_py_script(repo_dir):
    py_script_path = os.path.join(repo_dir, "open_repo.py")

    if os.path.exists(py_script_path):
        os.remove(py_script_path)
        print(f"Removed Python script from repository directory: {py_script_path}")
    else:
        print("Python script does not exist in the repository directory.")


def remove_config_file():
    if os.path.exists("config.json"):
        os.remove("config.json")
        print("Removed config.json from the root directory.")
    else:
        print("config.json does not exist in the root directory.")


def main():
    config = load_config()

    if config:
        repo_dir = config.get("repo_dir")

        remove_ahk_script()

        remove_py_script(repo_dir)

        remove_config_file()

    print("Removal process complete")


if __name__ == "__main__":
    main()
