from cx_Freeze import setup, Executable

options = {
    "build_exe": {
        "packages": ["chess"],  # Add any additional packages your script uses
    }
}

executables = [
    Executable("ofishv1h.py"),
]

setup(
    name="Ofish V1H",
    version="1.1",
    description="Ospiring to be a pyfish",
    executables=executables
)
