#Requires AutoHotkey v2.0

^!r:: { ; Ctrl + Alt + R to trigger
    Run("cmd.exe /k python path\to\repo\open_repo.py", "", "runas")
}
