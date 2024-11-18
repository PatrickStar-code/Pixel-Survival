from cx_Freeze import setup, Executable

import os

path = "./assets"
asset_list = os.listdir(path)
asset_list_completa = [os.path.join(path, asset).replace("\\", "/") for asset in asset_list]
print(asset_list_completa)

executables = [Executable("main.py")]
files = {"include_files": asset_list_completa, "packages": ["pygame"]}

setup(
    name="PixelSurvival",
    version="1.0",
    description="Pixel Survival app",
    options={"build_exe": {"packages": ["pygame"]}},
    executables=executables
)
