import os
import yaml
import re

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]
DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]

print("""
_________      _________ ___         v-0.3.1
______  / ________  __/  / / _______      __
_  __  /__  ___/_  /_   / /_  __ \_ | /| / /
/ /_/ /  (__  )_  __/  / / / /_/ /_ |/ |/ /
\__,_/  /____/ /_/    /_/  \____/____/|__/

      """)

print("Usage:")
print("dsflow COMMAND_NAME [options]")
print("")

commands = sorted([re.match("dsflow-(.*).py", f).group(1)
                   for f in os.listdir(DSFLOW_ROOT)
                   if (os.path.isfile(os.path.join(DSFLOW_ROOT, f)) and "dsflow-" in f)])

with open(os.path.join(DSFLOW_ROOT, "menu.yaml"), 'r') as f:
    menu_specs = yaml.load(f)


for cmd in commands:
    if cmd in menu_specs:
        print("    " + cmd.ljust(20) + "   {}".format(menu_specs[cmd]["short_description"]))
    else:
        print("    %s" % cmd)
