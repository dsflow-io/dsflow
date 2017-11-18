import sys
import os
import subprocess


pwd = os.environ["PWD"]
tmp_abs_path = os.path.join(pwd, "tmp")
datastore_abs_path = os.path.join(pwd, "datastore")
jobs_abs_path = os.path.join(pwd, "jobs")

DSFLOW_WORKSPACE = pwd

docker_compose_base_file = "dsflow/docker/base/docker-compose.yaml"
docker_compose_db = "dsflow/docker/db/docker-compose.yaml"
docker_compose_airflow = "dsflow/docker/airflow/docker-compose.yaml"
# sys.argv[1]

my_env = os.environ.copy()
my_env["DSFLOW_WORKSPACE"] = pwd

args = ["docker-compose",
        "-f", docker_compose_base_file,
        "-f", docker_compose_db,
        "-f", docker_compose_airflow,
        ]

# preview
subprocess.call(args + ["config"], env=my_env)

# "--volume=%s:/tmp:rw" % tmp_abs_path,
# "--volume=%s:/data:rw" % datastore_abs_path,
# "--volume=%s:/jobs:ro" % jobs_abs_path,


print(" ".join(args))

subprocess.call(args + ["up", "-d"], env=my_env)

subprocess.call(args + ["exec", "airflow", "/bin/bash"], env=my_env)
