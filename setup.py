from cx_Freeze import setup, Executable

target = Executable(
    script="ki c moi.py",
    base="Win32GUI",
    icon="assets/logo.ico"
    )

setup(
    name="Ki c moi ?",
    version="1.0",
    description="Ki c moi?",
    author="Yavan",
    executables=[target]
    )