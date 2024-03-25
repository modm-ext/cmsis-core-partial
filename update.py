import sys
import json
import shutil
import subprocess
from pathlib import Path
import urllib.request

source_paths = [
    "CMSIS/Core/Include/**/*.h",
    "LICENSE",
]

with urllib.request.urlopen("https://api.github.com/repos/arm-software/CMSIS_6/releases/latest") as response:
   tag = json.loads(response.read())["tag_name"]

# clone the repository
if "--fast" not in sys.argv:
    print("Cloning CMSIS_6 repository at tag {}...".format(tag))
    shutil.rmtree("cmsis_src", ignore_errors=True)
    subprocess.run("GIT_LFS_SKIP_SMUDGE=1 git clone --depth=1 --branch {} ".format(tag) +
                   "https://github.com/arm-software/CMSIS_6.git cmsis_src", shell=True)

# remove the sources in this repo
shutil.rmtree("CMSIS", ignore_errors=True)
Path("LICENSE.txt").unlink(missing_ok=True)
Path("LICENSE").unlink(missing_ok=True)

print("Copying CMSIS_6 sources...")
for pattern in source_paths:
    for path in Path("cmsis_src").glob(pattern):
        if not path.is_file(): continue
        dest = path.relative_to("cmsis_src")
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(dest)
        # Copy, normalize newline and remove trailing whitespace
        with path.open("r", newline=None, encoding="utf-8", errors="replace") as rfile, \
                           dest.open("w", encoding="utf-8") as wfile:
            wfile.writelines(l.rstrip()+"\n" for l in rfile.readlines())

subprocess.run("git add CMSIS LICENSE", shell=True)
if subprocess.call("git diff-index --quiet HEAD --", shell=True):
    subprocess.run('git commit -m "Update CMSIS to {}"'.format(tag), shell=True)
