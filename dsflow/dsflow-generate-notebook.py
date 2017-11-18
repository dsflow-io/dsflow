import sys
import os
import subprocess

# Input parameters
input_parameters = sys.argv[1:]

# Paths, ids and env. variables
pwd = os.environ["PWD"]
datastore_abs_path = os.path.join(pwd, "datastore")
jobs_abs_path = os.path.join(pwd, "jobs")

docker_image_dir = "dsflow-notebook-generator"
docker_image_id = "dsflow/%s" % docker_image_dir

# Build docker image
print("\n========== building docker image ===========")
subprocess.call(["docker",
                 "build",
                 "-t", docker_image_id,
                 "-f", "dsflow/docker/" + docker_image_dir + "/Dockerfile",
                 "./dsflow",
                 ])

# Run dsflow assistant in docker container
args = [
    "docker",
    "run",
    "-i",
    "--volume=%s:/data:rw" % datastore_abs_path,
    "--volume=%s:/jobs:rw" % jobs_abs_path,
    "--env=DSFLOW_DATASTORE_ROOT=/data",
    "--env=DSFLOW_JOBS_ROOT=/jobs",
    "--env=DSFLOW_ROOT=/usr/src/app",
    docker_image_id,
    "python",
    "dsflow-generate-notebook.py"
] + input_parameters

print("\n========== docker run command ===========")
print(" ".join(args))

print("\n========== running docker container ===========")
subprocess.call(args)
