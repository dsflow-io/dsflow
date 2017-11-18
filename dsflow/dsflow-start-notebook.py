import sys
import os
import subprocess


pwd = os.environ["PWD"]
tmp_abs_path = os.path.join(pwd, "tmp")
datastore_abs_path = os.path.join(pwd, "datastore")
jobs_abs_path = os.path.join(pwd, "jobs")

DSFLOW_WORKSPACE = pwd

docker_compose_file = "dsflow/docker/docker-compose-all.yaml"
# sys.argv[1]

my_env = os.environ.copy()
my_env["DSFLOW_ROOT"] = "/Users/pmleveque/dsflow/master/dsflow-cli"
my_env["DSFLOW_WORKSPACE"] = pwd

args = ["docker-compose",
        "-f",
        docker_compose_file,
        "up",
        ]

subprocess.call(["docker-compose",
        "-f",
        docker_compose_file,
        "config"], env=my_env)

# "--volume=%s:/tmp:rw" % tmp_abs_path,
# "--volume=%s:/data:rw" % datastore_abs_path,
# "--volume=%s:/jobs:ro" % jobs_abs_path,


print(" ".join(args))

subprocess.call(args, env=my_env)
