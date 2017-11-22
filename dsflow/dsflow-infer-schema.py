import sys
import os
import subprocess

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

# Input parameters
input_parameters = sys.argv[1:]

# Paths, ids and env. variables
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]
datastore_abs_path = os.path.join(DSFLOW_WORKSPACE, "datastore")
jobs_abs_path = os.path.join(DSFLOW_WORKSPACE, "jobs")

docker_image_dir = "dsflow-schema-generator"
docker_image_id = "dsflow/%s" % docker_image_dir

image_id = "dsflow-schema-generator"
docker_compose_file = "dsflow/docker/%s/docker-compose.yaml" % image_id

# Rebuild docker image if --build argument is passed
if input_parameters and input_parameters[0] == "--build":
    subprocess.call([
        "docker-compose",
        "-f", docker_compose_file,
        "config"])

    subprocess.call([
        "docker-compose",
        "-f", docker_compose_file,
        "build"])

    input_parameters = input_parameters[1:]

args = [
    "docker-compose",
    "-f", docker_compose_file,
    "run",
    "schema-generator",
    "python",
    "python_scripts/infer_schema.py"
] + input_parameters

print("\n========== preview docker run command ===========")
print(" ".join(args))

print("\n========== running docker container ===========")
subprocess.call(args)

print("\n========== script output ===========")
output_path = DSFLOW_WORKSPACE + "/tmp/schema-generator/schema.json"

print(output_path)
print(open(output_path, 'r').read())
