import PyInstaller.__main__

PyInstaller.__main__.run(
    ["..\\AddonsUpdater.py", "--onefile", "--icon=..\\res\\icon.ico", "--distpath=..\\"]
)
