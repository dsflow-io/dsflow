import sys
import os
import subprocess

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]

docker_compose_base_file = DSFLOW_ROOT + "/docker/base/docker-compose.yaml"
docker_compose_dash = DSFLOW_ROOT + "/docker/dash/docker-compose.yaml"
# sys.argv[1]

my_env = os.environ.copy()

args = ["docker-compose",
        "-f", docker_compose_base_file,
        "-f", docker_compose_dash,
        ]

# preview
subprocess.call(args + ["config"], env=my_env)

print(" ".join(args))

subprocess.call(args + ["run", "--service-ports", "dash"], env=my_env)
