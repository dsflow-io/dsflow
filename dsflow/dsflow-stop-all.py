import sys
import os
import subprocess


docker_compose_file = "dsflow/docker/base/docker-compose.yaml"
# sys.argv[1]

args = ["docker-compose",
        "-f",
        docker_compose_file,
        "down",
        "--remove-orphans"
        ]

print(" ".join(args))

subprocess.call(args)
