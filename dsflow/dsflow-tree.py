import sys
import os
import subprocess

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]

docker_compose_assistant = DSFLOW_ROOT + "/docker/assistant/docker-compose.yaml"

directory = sys.argv[1] if len(sys.argv) > 1 else "/data"
depth = sys.argv[2] if len(sys.argv) > 2 else "3"

my_env = os.environ.copy()

args = ["docker-compose",
        "-f", docker_compose_assistant,
        ]

subprocess.call(args + ["up", "-d"])
subprocess.call(args + ["exec", "assistant", "tree", directory, "-dCL", depth], env=my_env)
