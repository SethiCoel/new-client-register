import sys
from cx_Freeze import setup, Executable

#Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": []}


#GUI applications require a different base on Windows (the default is for
#a console application).
# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(
    name="Registro de Clientes",
    version="0.1",
    description="Registra dados de clientes",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", base=None, icon="icon.ico")]
)