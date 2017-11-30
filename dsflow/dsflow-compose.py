import sys
import os
import subprocess

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]
DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]

# Input parameters
dsflow_service_name = sys.argv[1]
docker_compose_file = DSFLOW_ROOT + "/docker/%s/docker-compose.yaml" % dsflow_service_name

input_parameters = sys.argv[2:]

my_env = os.environ.copy()

args = ["docker-compose",
        "-f", docker_compose_file,
        ]

# preview
subprocess.call(args + ["config"], env=my_env)

print(" ".join(args))

subprocess.call(args + ["up", "--build", "-d"], env=my_env)

subprocess.call(args + ["exec", dsflow_service_name, "/bin/bash"], env=my_env)
