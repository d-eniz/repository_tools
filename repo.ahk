#Requires AutoHotkey v2.0

^!r:: { ; Ctrl + Alt + R to trigger
    ; Run the Python script in a new elevated (admin) command prompt window
    Run("cmd.exe /k python D:/test\open_repo.py", "", "runas")
}
