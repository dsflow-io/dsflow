import click
import subprocess
import shlex
import os
import errno
import nbformat as nbf
import yaml
from jinja2 import Template, Environment, FileSystemLoader
import json
import datetime as dt
from configparser import ConfigParser
from pprint import *
import webbrowser
import time
import requests
import textwrap
import glob
import logging

from . import DSFLOW_ROOT


LIVY_HOST = 'http://localhost:8998'


def get_flows_path():
    if "HOSTNAME" in os.environ and os.environ["HOSTNAME"] == "spark-master":
        return "/home/jovyan/flows"
    else:
        # FIXME: add this property to config file
        # return get_config("paths.dsflow_flows_path")
        return os.path.join(get_app_path(), "flows")


def log_info(log_string):
    click.echo("INFO - %s" % log_string)


def get_datastore_path():
    if "HOSTNAME" in os.environ and os.environ["HOSTNAME"] == "spark-master":
        return "/data"
    else:
        return get_config("DATASTORE_ROOT")


def get_app_path():
    return get_config("ROOT")


def get_jobs_path():
    return get_config("JOBS_ROOT")


def show_instructions(instructions):
    click.secho(instructions, fg="blue")


def get_config(name):
    return os.environ["DSFLOW_" + name.upper()]


def mkdir_if_needed(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


# FIXME don't use subprocess.call() but instead:
# https://docs.python.org/2/distutils/apiref.html#distutils.dir_util.copy_tree


class DsflowGenerator:
    def __init__(self, app_path=None):
        if app_path:
            self.app_path = app_path
        else:
            # fixme: this should fail if not running from app root
            self.app_path = get_app_path()

        self.jinja_env = Environment(
            loader=FileSystemLoader(os.path.join(DSFLOW_ROOT, '..', 'templates'))
        )


    def mkdir_and_log(self, dir_path):
        full_path = os.path.join(self.app_path, dir_path)
        subprocess.call(["mkdir", "-p", full_path])

        dir_path_formatted = dir_path.replace(self.app_path + "/", "")
        click.echo("     new directory    {}/".format(dir_path_formatted))


    def copy_file_and_log(self, file_path, target_dir):
        """copy from dsflow framework dir to dsflow app"""

        read_path = os.path.join(DSFLOW_ROOT, "templates", file_path)
        write_path = os.path.join(self.app_path, target_dir, file_path)
        subprocess.call(["cp", read_path, write_path])

        click.echo("     new file         {}/{}".format(target_dir, file_path))


    def generate_file_from_template(self, template_path, target_path, **values):
        """renders files from templates/ dir, using **kwargs"""

        t = self.jinja_env.get_template(template_path)

        write_path = os.path.join(self.app_path, target_path)

        with open(write_path, 'w') as f:
            f.write(t.render(**values))

        click.echo("     new file         {}".format(target_path))


    def copy_dir_and_log(self, source_dir, target_dir):
        """copy from dsflow framework dir to dsflow app"""

        read_path = os.path.join(DSFLOW_ROOT, "templates", source_dir)
        write_path = os.path.join(self.app_path, target_dir)
        subprocess.call(["cp", "-nr", read_path, write_path])

        click.echo("     new files        {} ...".format(target_dir))


# TODO return error message if Spark in not running
def execute_sql(query):
    """Run Spark SQL code in a container, through Livy"""

    data = {'kind': 'pyspark3'}
    headers = {'Content-Type': 'application/json'}
    log_info(requests.get(LIVY_HOST + "/sessions").json())

    # TODO retrive newest session id
    LIVY_SESSION_ID = 0

    statements_url = "{}/sessions/{}/statements".format(LIVY_HOST,
                                                        LIVY_SESSION_ID)

    log_info("statements_url = " + statements_url)

    data = {
      'code': 'spark.sql("""%s""").show()' % query
    }

    log_info("data = %s" % data)

    r = requests.post(statements_url, data=json.dumps(data), headers=headers)
    log_info(pformat(r.json()))

    job_url = statements_url + "/" + str(r.json()["id"])
    log_info("job_url = " + job_url)

    time.sleep(0.1)

    while requests.get(job_url, headers=headers).json()["state"] == "running":
        log_info("waiting...")
        time.sleep(1)

    click.echo(requests.get(job_url).json()["output"]["data"]["text/plain"])
