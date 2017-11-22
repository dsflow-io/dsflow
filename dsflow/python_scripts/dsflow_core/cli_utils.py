import os

def validate_env():
    if "DSFLOW_ROOT" not in os.environ:
        raise(Exception("Environment variable DSFLOW_ROOT must be set."))

    if "DSFLOW_WORKSPACE" not in os.environ:
        raise(Exception("Environment variable DSFLOW_WORKSPACE must be set.\nIt's necessary for docker-compose.yaml"))
