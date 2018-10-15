# Script is tested on OS X 10.12 and Ubuntu 12.04 LTS
# YOUR MILEAGE MAY VARY

# convert all files to unix line endings
find CMSIS -path "*/.git" -prune -o -type f -print0 | xargs -0 -I file dos2unix file file

# yay, computers
export LANG=C
export LC_CTYPE=C
export LC_ALL=C
# remove all trailing whitespace from the CMSIS files
find CMSIS -path "*/.git" -prune -o -type f -print0 | xargs -0 sed -i 's/\s*$//'
