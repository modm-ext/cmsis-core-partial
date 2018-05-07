# Script is tested on OS X 10.12
# YOUR MILEAGE MAY VARY

import sys
import shutil
import subprocess
from pathlib import Path

source_paths = [
    Path("CMSIS/Core/Include"),
    Path("CMSIS/DSP/Include"),
    Path("CMSIS/DSP/Source")
]

# clone the repository
if not Path("CMSIS_5").exists():
    subprocess.run("git clone https://github.com/arm-software/CMSIS_5.git", shell=True)

# remove the sources in this repo
if Path("CMSIS").exists():
    shutil.rmtree("CMSIS")

for path in source_paths:
    # create path and parents
    path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(str("CMSIS_5" / path), str(path))
