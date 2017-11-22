import sys
import os
import subprocess

from python_scripts.dsflow_core import models

pwd = os.environ["PWD"]
tmp_abs_path = os.path.join(pwd, "tmp")
datastore_abs_path = os.path.join(pwd, "datastore")
jobs_abs_path = os.path.join(pwd, "jobs")

DSFLOW_WORKSPACE = pwd

docker_compose_assistant = "dsflow/docker/assistant/docker-compose.yaml"

directory = sys.argv[1] if len(sys.argv) > 1 else "/data"
depth = sys.argv[2] if len(sys.argv) > 2 else "2"

my_env = os.environ.copy()
my_env["DSFLOW_WORKSPACE"] = pwd

args = ["docker-compose",
        "-f", docker_compose_assistant,
        ]

subprocess.call(args + ["up", "-d"])
subprocess.call(args + ["exec", "assistant", "tree", directory, "-dCL", depth], env=my_env)
