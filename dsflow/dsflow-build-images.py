import sys
import os
import subprocess

import dsflow_core_lib

pwd = os.environ["PWD"]

# TODO: automatically find all images in dsflow/docker/
docker_compose_base_file = "dsflow/docker/base/docker-compose.yaml"
docker_compose_dash = "dsflow/docker/dash/docker-compose.yaml"
docker_compose_db = "dsflow/docker/db/docker-compose.yaml"
docker_compose_airflow = "dsflow/docker/airflow/docker-compose.yaml"
# sys.argv[1]

my_env = os.environ.copy()
my_env["DSFLOW_WORKSPACE"] = pwd

args = ["docker-compose",
        "-f", docker_compose_base_file,
        "-f", docker_compose_db,
        "-f", docker_compose_dash,
        "-f", docker_compose_airflow
        ]

# preview
subprocess.call(args + ["config"], env=my_env)

print(" ".join(args))

subprocess.call(args + ["build"], env=my_env)
