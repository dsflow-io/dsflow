from os import listdir, environ
from os.path import isfile, join
import re

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_WORKSPACE = environ["DSFLOW_WORKSPACE"]
DSFLOW_ROOT = environ["DSFLOW_ROOT"]

print("=== available commands ===")

commands = sorted([re.match("dsflow-(.*).py", f).group(1)
                   for f in listdir(DSFLOW_ROOT)
                   if (isfile(join(DSFLOW_ROOT, f)) and "dsflow-" in f)])

for cmd in commands:
    print(cmd)
