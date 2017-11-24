import sys
import os
import subprocess
import yaml
import json

from python_scripts.dsflow_core.cli_utils import validate_env

validate_env()

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]

job_name = sys.argv[1]
input_parameters = sys.argv[2:]

tmp_abs_path = os.path.join(DSFLOW_WORKSPACE, "tmp")
datastore_abs_path = os.path.join(DSFLOW_WORKSPACE, "datastore")
jobs_abs_path = os.path.join(DSFLOW_WORKSPACE, "jobs")

print("job_name :", job_name)
print("input_parameters :", input_parameters)

job_specs_path = os.path.join(jobs_abs_path, job_name, "job_specs.yaml")
job_specs_raw = yaml.load(open(job_specs_path, 'r'))

try:
    job_parameters = {job_specs_raw["job_parameters"][key]: input_parameters[key]
                      for key in range(len(input_parameters))}

    # FIXME: this is hardcoded for now
    job_specs = job_specs_raw.copy()

    if "task_specs" in job_specs:
        for key in job_specs["task_specs"]:
            job_specs["task_specs"][key] = \
                job_specs["task_specs"][key].replace("{{ ds }}", job_parameters["ds"])

except:
    raise(Exception("missing parameters:", job_specs_raw["job_parameters"]))


print(job_parameters)
print(job_specs)

script_container_path = os.path.join("/jobs", job_name, job_specs["script"])

my_env = os.environ.copy()

if job_specs["class"] == "JupyterNotebook":
    image_id = "base"  # FIXME

    docker_compose_file = DSFLOW_ROOT + "/docker/%s/docker-compose.yaml" % image_id

    args = [
        "docker-compose",
        "-f", docker_compose_file,
        "run",
        # "-i",
        # "--network=dsflow",
        # "--volume=%s:/tmp:rw" % tmp_abs_path,
        "-v", "%s:/data:rw" % datastore_abs_path,
        "-v", "%s:/jobs:ro" % jobs_abs_path,
        "-e", "TASK_SPECS=%s" % json.dumps(job_specs["task_specs"]).replace(" ", ""),
        "pyspark",
        "jupyter",
        "nbconvert",
        "--to=html",
        "--execute",
        "/%s" % script_container_path,
        "--ExecutePreprocessor.allow_errors=True",
        "--ExecutePreprocessor.timeout=3600",
        # "'--ExecutePreprocessor.kernel_name='"'"'python3'"'"''",
        "--output-dir",
        "/data/job_runs/%s" % job_name,
    ]

    print(" ".join(args))

    subprocess.call(args, env=my_env)

elif job_specs["class"] == "CommandLineTool":
    image_id = "base"

    docker_compose_file = DSFLOW_ROOT + "/docker/%s/docker-compose.yaml" % image_id

    args = [
        "docker-compose",
        "-f", docker_compose_file,
        "run",
        "pyspark",
        "." + script_container_path,
        job_specs["task_specs"]["source_path"],
        job_specs["task_specs"]["sink_path"]  # FIXME input / ouput params shouldn't be hardcoded
    ]

    print(" ".join(args))

    subprocess.call(args, env=my_env)


elif job_specs["class"] == "PlotlyDashApplication":
    image_id = "dash"

    docker_compose_file = DSFLOW_ROOT + "/docker/%s/docker-compose.yaml" % image_id

    args = [
        "docker-compose",
        "-f", docker_compose_file,
        "run",
        "--service-ports",  # expose port (false by default with docker-compose run)
        "dash",
        "python",
        script_container_path
    ]

    print(" ".join(args))

    subprocess.call(args, env=my_env)

else:
    raise(Exception("unknown job class"))
