import sys
import os
import subprocess

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]

docker_compose_base_file = DSFLOW_ROOT + "/docker/base/docker-compose.yaml"
docker_compose_db = DSFLOW_ROOT + "/docker/db/docker-compose.yaml"
docker_compose_airflow = DSFLOW_ROOT + "/docker/airflow/docker-compose.yaml"
# sys.argv[1]

my_env = os.environ.copy()

args = ["docker-compose",
        "-f", docker_compose_base_file,
        "-f", docker_compose_db,
        "-f", docker_compose_airflow,
        ]

print("\n========== calling docker-compose ====================")
print(" ".join(args))
subprocess.call(args + ["up", "-d"], env=my_env)

print("\nAirflow web interface is accessible at http://localhost:8081/")
print("Hint: `dsflow airflow-bash` will give you access to "
      "airflow container bash")
