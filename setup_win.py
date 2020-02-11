from cx_Freeze import setup, Executable

base = None    

executables = [Executable("bot.py", base=base)]

packages = ["idna", "os", "sys", "selenium", "time", "csv", "json", "sqlite3"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "imstrongbot",
    options = options,
    version = "2",
    description = 'Simple Whatsapp Bot',
    executables = executables
)