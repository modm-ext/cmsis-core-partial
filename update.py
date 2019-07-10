# Script is tested on OS X 10.12
# YOUR MILEAGE MAY VARY

import sys
import shutil
import subprocess
from pathlib import Path

source_paths = [
    "CMSIS/Core/Include",
    "CMSIS/DSP/Include",
    "CMSIS/DSP/Source",
    "CMSIS/DSP/Examples/ARM/*_example/*.c",
    "CMSIS/DSP/Examples/ARM/*_example/*.h",
]

# clone the repository
print("Cloning CMSIS_5 repository...")
if not Path("CMSIS_5").exists():
    subprocess.run("git clone https://github.com/arm-software/CMSIS_5.git", shell=True)

# remove the sources in this repo
if Path("CMSIS").exists():
    shutil.rmtree("CMSIS")

print("Copying CMSIS_5 sources...")
for pattern in source_paths:
    for path in Path("CMSIS_5").glob(pattern):
        dest = path.relative_to("CMSIS_5")
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.is_dir():
            shutil.copytree(path, dest)
        else:
            shutil.copy2(path, dest)

print("Normalizing CMSIS_5 newlines and whitespace...")
subprocess.run("sh ./post_script.sh > /dev/null 2>&1", shell=True)
