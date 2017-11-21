import sys
import os
import subprocess

from dsflow_core.cli_utils import validate_env

validate_env()

# Input parameters
input_parameters = sys.argv[1:]

# Paths, ids and env. variables
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]
datastore_abs_path = os.path.join(DSFLOW_WORKSPACE, "datastore")
jobs_abs_path = os.path.join(DSFLOW_WORKSPACE, "jobs")

docker_image_dir = "dsflow-notebook-generator"
docker_image_id = "dsflow/%s" % docker_image_dir

image_id = "dsflow-notebook-generator"
docker_compose_file = "dsflow/docker/%s/docker-compose.yaml" % image_id

# Rebuild docker image
if input_parameters and input_parameters[0] == "--build":
    subprocess.call([
        "docker-compose",
        "-f", docker_compose_file,
        "build"])

    input_parameters = input_parameters[1:]

args = [
    "docker-compose",
    "-f", docker_compose_file,
    "run",
    "notebook-generator",
    "python",
    "dsflow-generate-notebook.py"
] + input_parameters

print("\n========== preview docker run command ===========")
print(" ".join(args))

print("\n========== running docker container ===========")
subprocess.call(args)
