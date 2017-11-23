import sys
import os
import subprocess

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]

docker_compose_file = DSFLOW_ROOT + "/docker/base/docker-compose.yaml"
# sys.argv[1]

my_env = os.environ.copy()

args = ["docker-compose",
        "-f",
        docker_compose_file,
        "down",
        "--remove-orphans"
        ]

print(" ".join(args))

subprocess.call(args, env=my_env)
