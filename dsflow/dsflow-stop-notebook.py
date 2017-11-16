import sys
import os
import subprocess


docker_compose_file = "dsflow/docker/docker-compose-all.yaml"
# sys.argv[1]

args = ["docker-compose",
        "-f",
        docker_compose_file,
        "down",
        ]

print(" ".join(args))

subprocess.call(args)
