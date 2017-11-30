import sys
import os
import subprocess
from python_scripts.poyo import parse_string
import json

from python_scripts.dsflow_core.cli_utils import validate_env

# make sure environment variables are set
validate_env()

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]
DSFLOW_WORKSPACE = os.environ["DSFLOW_WORKSPACE"]

if len(sys.argv) < 2:
    sys.exit("Usage: dsflow run JOB_NAME [JOB_PARAMETERS]"
             "\n\nShow list of jobs: `ls jobs`")

job_name = sys.argv[1]
input_parameters = sys.argv[2:]

tmp_abs_path = os.path.join(DSFLOW_WORKSPACE, "tmp")
datastore_abs_path = os.path.join(DSFLOW_WORKSPACE, "datastore")
jobs_abs_path = os.path.join(DSFLOW_WORKSPACE, "jobs")

print("======================================================",
      "\nRunning job", job_name,
      "\nwith input parameters", input_parameters)


job_specs_path = os.path.join(jobs_abs_path, job_name, "job_specs.yaml")

try:
    with open(job_specs_path, 'r') as f:
        job_specs_raw = parse_string(f.read())
except FileNotFoundError:
    sys.exit("""\nERROR: Job does not exist, or job_specs.yaml is missing.

Usage: dsflow run JOB_NAME [JOB_PARAMETERS]
""")

try:
    job_parameters = {job_specs_raw["job_parameters"][key]: input_parameters[key]
                      for key in range(len(input_parameters))}

    # FIXME: use a jinja template instead of a python str.replace() method.
    job_specs = job_specs_raw.copy()

    if "task_specs" in job_specs:
        for parameter_name in job_specs_raw["job_parameters"]:
            for key in job_specs["task_specs"]:
                job_specs["task_specs"][key] = job_specs["task_specs"][key] \
                 .replace("{{ %s }}" % parameter_name,
                          job_parameters[parameter_name])

except KeyError:
    if "job_parameters" not in job_specs_raw:
        sys.exit("\nERROR: this job doesn't accept parameters")
    else:
        sys.exit("\nERROR: wrong parameters. Acceptable parameters are: %s"
                 % job_specs_raw["job_parameters"])

except IndexError:
    sys.exit("\nERROR: wrong parameters. Acceptable parameters are: %s"
             % job_specs_raw["job_parameters"])

print("\n========== job parameters ============================")
print(job_parameters)

print("\n========== job instance specifications ===============")
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
        "/data/job_runs/%s" % job_name,  # FIXME add partition
    ]

    print("\n========== calling docker-compose ====================")
    print(" ".join(args))

    print("\n========== job execution logs ========================")
    subprocess.call(args, env=my_env)

    print("\n========== job output ================================")
    print("Notebook execution logs added to datastore/job_runs/%s" % job_name)
    print("Job output data saved to %s"
          % job_specs["task_specs"]["sink_path"]
          .replace("/data/", "datastore/"))

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

    print("\n========== calling docker-compose ====================")
    print(" ".join(args))

    print("\n========== job execution logs ========================")
    subprocess.call(args, env=my_env)

    print("\n========== job output ================================")
    print("Job output data saved to %s"
          % job_specs["task_specs"]["sink_path"]
          .replace("/data/", "datastore/"))

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

    print("\n========== calling docker-compose ====================")
    print(" ".join(args))

    print("\n    dashboard will be accessible at http://localhost:8050/")
    print("\n    (Press CTRL+C to quit)")


    print("\n========== job execution logs ========================")
    subprocess.call(args, env=my_env)

else:
    raise(Exception("unknown job class"))
