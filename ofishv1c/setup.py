from cx_Freeze import setup, Executable

options = {
    "build_exe": {
        "packages": ["chess"],  # Add any additional packages your script uses
    }
}

executables = [
    Executable("ofishv1c.py"),
]

setup(
    name="AsPy Fish",
    version="1.0",
    description="Ospiring to be a pyfish",
    executables=executables
)
