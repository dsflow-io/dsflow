import sys
import os
import subprocess


job_name = sys.argv[1]
input_parameter = sys.argv[2]

pwd = os.environ["PWD"]
tmp_abs_path = os.path.join(pwd, "tmp")
datastore_abs_path = os.path.join(pwd, "datastore")
jobs_abs_path = os.path.join(pwd, "jobs")
docker_image_id = "jupyter/pyspark-notebook"

my_env = os.environ.copy()
my_env["DSFLOW_WORKSPACE"] = pwd

docker_compose_file = "dsflow/docker/base/docker-compose.yaml"

print("job_name :", job_name)
print("input_parameter :", input_parameter)

args = [
    "docker-compose",
    "-f", docker_compose_file,
    "run",
    # "-i",
    # "--network=dsflow",
    # "--volume=%s:/tmp:rw" % tmp_abs_path,
    "-v", "%s:/data:rw" % datastore_abs_path,
    "-v", "%s:/jobs:ro" % jobs_abs_path,
    "-e", "INPUT_PARAMETER=%s" % input_parameter,
    "pyspark",
    "jupyter",
    "nbconvert",
    "--to=html",
    "--execute",
    "/%s" % job_name,
    "--ExecutePreprocessor.allow_errors=True",
    "--ExecutePreprocessor.timeout=3600",
    # "'--ExecutePreprocessor.kernel_name='"'"'python3'"'"''",
    "--output-dir",
    "/data/job_runs/%s" % job_name,
]

print(" ".join(args))

subprocess.call(args, env=my_env)
