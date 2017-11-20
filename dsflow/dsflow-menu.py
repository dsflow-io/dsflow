from os import listdir
from os.path import isfile, join
import re

print("=== available commands ===")

commands = sorted([re.fullmatch("dsflow-(.*).py", f)[1]
 for f in listdir("dsflow")
 if (isfile(join("dsflow", f)) and "dsflow-" in f)])

for cmd in commands:
    print(cmd)
