import sys
import os
import subprocess


pwd = os.environ["PWD"]
tmp_abs_path = os.path.join(pwd, "tmp")
datastore_abs_path = os.path.join(pwd, "datastore")
jobs_abs_path = os.path.join(pwd, "jobs")

DSFLOW_WORKSPACE = pwd

docker_compose_base_file = "dsflow/docker/base/docker-compose.yaml"
docker_compose_dash = "dsflow/docker/dash/docker-compose.yaml"
# sys.argv[1]

my_env = os.environ.copy()
my_env["DSFLOW_WORKSPACE"] = pwd

args = ["docker-compose",
        "-f", docker_compose_base_file,
        "-f", docker_compose_dash,
        ]

# preview
subprocess.call(args + ["config"], env=my_env)

# "--volume=%s:/tmp:rw" % tmp_abs_path,
# "--volume=%s:/data:rw" % datastore_abs_path,
# "--volume=%s:/jobs:ro" % jobs_abs_path,


print(" ".join(args))

# subprocess.call(args + ["build"], env=my_env)

subprocess.call(args + ["run", "dash", "/bin/sh"], env=my_env)
