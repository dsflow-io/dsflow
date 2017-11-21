import sys
import os
import subprocess

from dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]

docker_compose_base_file = "dsflow/docker/base/docker-compose.yaml"
docker_conpose_db = "dsflow/docker/db/docker-compose.yaml"
# sys.argv[1]

my_env = os.environ.copy()

args = ["docker-compose",
        "-f", docker_compose_base_file,
        "-f", docker_conpose_db,
        ]

subprocess.call(args + ["config"], env=my_env)

# "--volume=%s:/tmp:rw" % tmp_abs_path,
# "--volume=%s:/data:rw" % datastore_abs_path,
# "--volume=%s:/jobs:ro" % jobs_abs_path,


print(" ".join(args))

subprocess.call(args + ["up", "-d"], env=my_env)
