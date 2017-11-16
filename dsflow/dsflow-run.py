import sys
import os
import subprocess

# Example:
"""
DOC:

python dsflow/dsflow-run.py jobs/table-people/create.ipynb ds=2017-11-09

"""

job_name = sys.argv[1]
input_parameter = sys.argv[2]

pwd = os.environ["PWD"]
tmp_abs_path = os.path.join(pwd, "tmp")
datastore_abs_path = os.path.join(pwd, "datastore")
jobs_abs_path = os.path.join(pwd, "jobs")
docker_image_id = "jupyter/pyspark-notebook"

print("job_name :", job_name)
print("input_parameter :", input_parameter)

args = [
    "docker",
    "run",
    "-i",
    "--volume=%s:/tmp:rw" % tmp_abs_path,
    "--volume=%s:/data:rw" % datastore_abs_path,
    "--volume=%s:/jobs:ro" % jobs_abs_path,
    "--workdir=/tmp",
    # "--read-only=true",
    # "--user=502:20",
    # "--rm",
    # "--env=TMPDIR=/tmp",
    # "--env=HOME=/tmp",
    "--env=INPUT_PARAMETER=%s" % input_parameter,
    docker_image_id,
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

subprocess.call(args)
