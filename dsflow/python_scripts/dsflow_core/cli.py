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
import sys
import docker
import click_spinner
from envparse import env

from . import DSFLOW_ROOT
from .utils import *
from .models import *

print("""
_________      _________ ___    v0.3 alpha
______  / ________  __/  / / _______      __
_  __  /__  ___/_  /_   / /_  __ \_ | /| / /
/ /_/ /  (__  )_  __/  / / / /_/ /_ |/ |/ /
\__,_/  /____/ /_/    /_/  \____/____/|__/

      """)


@click.group()
def cli():
    pass


@cli.command(short_help="create new dsflow application")
@click.argument("app-name")
def new(app_name):
    """dsflow app initialization"""

    if "VIRTUAL_ENV" not in os.environ:
        raise Exception("Please run dsflow in a virtual environment")

    app_path = os.environ["PWD"] + "/{}".format(app_name)
    gen = DsflowGenerator(app_path=app_path)

    click.echo("Creating dsflow app [%s]........." % app_name)

    click.echo("     app root = {dsflow_app_path}".format(
        dsflow_app_path=app_path,
        ))

    gen.mkdir_and_log("config")

    gen.generate_file_from_template(os.path.join("config", "config.cfg.j2"),
                                os.path.join("config", "config.cfg"),
                                dsflow_root=DSFLOW_ROOT,
                                dsflow_app_path=app_path
                                )

    gen.copy_dir_and_log("config/", "config/")
    gen.mkdir_and_log("adhoc")
    gen.mkdir_and_log("datastore")
    gen.mkdir_and_log("datastore/raw")
    gen.mkdir_and_log("datastore/tables")
    gen.mkdir_and_log("environments")
    gen.mkdir_and_log("flows")
    gen.mkdir_and_log("templates/adhoc")
    gen.copy_dir_and_log("adhoc/", "templates/adhoc/")
    gen.mkdir_and_log("templates/flows")

    show_instructions("\nNext steps:\n`cd {}/`\n`dsflow start`\n`dsflow generate`\n"
                      .format(app_name))


@cli.command(short_help="list existing datasets...")
def list():
    """List existing datasets"""

    log_info("list of sub-directories of %s:" % get_datastore_path())
    datastore_path = get_datastore_path()

    for (directory, files, _) in os.walk(get_datastore_path()):
        click.echo(directory.replace(datastore_path, "datastore:"))


@click.option("--build", is_flag=True)
@click.option("--docker-compose-file", "-f", required=False)
@cli.command(short_help="Launch Spark and notebooks")
def start(build, docker_compose_file):
    """Launch Spark and notebooks in browser"""

    if not docker_compose_file:
        docker_compose_file = get_config("devops.docker_compose_file")

    docker_compose_abspath = os.path.abspath(docker_compose_file)

    # If the file is not found in the dsflow app, look in the dsflow root
    if not os.path.isfile(docker_compose_abspath):
        docker_compose_abspath = os.path.join(DSFLOW_ROOT, docker_compose_file)

    # .env is required by docker-compose
    # TODO: move this code to `dsflow start`
    with open(os.path.join(get_app_path(), ".env"), "w") as f:
        f.write("DSFLOW_WORKSPACE=" + get_app_path() + "\n")
        f.write("DSFLOW_ROOT=" + DSFLOW_ROOT + "\n")
        f.write("DOCKER_COMPOSE_FILE=" + docker_compose_abspath)

        click.echo("     new file         .env")

    # @todo Make sure it's not running already

    start_cmd = ["docker-compose",
                 "-f", docker_compose_abspath,
                 "up",
                 "-d",
                 ]

    if build:
        start_cmd += ["--build"]

    subprocess.call(start_cmd)

    time.sleep(1)

    show_instructions("\nDsflow interactive environment available at http://localhost:8888/ with password `green3`\n")

    # time.sleep(3)
    #
    # webbrowser.open('http://localhost:8888', new=3)


@cli.command(short_help="Stop Spark and notebooks")
def stop():
    """Launch Spark and notebooks in browser"""

    env.read_envfile('.env')

    dockercompose_file_path = os.path.join(DSFLOW_ROOT,
                                           os.environ["DOCKER_COMPOSE_FILE"])

    subprocess.call(["docker-compose",
                     "-f", dockercompose_file_path,
                     "down"])


@cli.command(short_help="Show docker logs")
def logs():
    """Display docker logs"""

    docker_compose_file = get_config("devops.docker_compose_file")

    subprocess.call(["docker-compose",
                     "-f", os.path.join(DSFLOW_ROOT, docker_compose_file),
                     "logs"])


@cli.command(short_help="convert notebook NOTEBOOK_NAME into a task")
@click.argument("notebook-name")
def transform(notebook_name):
    """Convert notebook NOTEBOOK_NAME into a task.
    WARNING!
    Currently, it only converts the notebook into a Python file,
    but does not create the task.
    """

    input_file = 'flows/%s.ipynb' % notebook_name
    output_file = 'flows/%s.py' % notebook_name
    click.echo("will create %s" % output_file)

    mkdir_if_needed(filename=output_file)

    # if os.path.isfile(output_file):
    #     raise Exception("File already exists. You can edit it using `dsflow notebooks`")

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        nb = json.load(infile)
        if nb["nbformat"] >= 4:
            for i, cell in enumerate(nb["cells"]):
                # outfile.write("#cell "+str(i)+"\n")
                if cell["cell_type"] == "code":
                    outfile.write("# <codecell>\n\n")
                    for line in cell["source"]:
                        outfile.write(line)
                else:
                    outfile.write("# <markdowncell>\n\n")
                    for line in cell["source"]:
                        outfile.write("# " + line)
                outfile.write('\n\n')


flow_templates_dir = os.path.join(DSFLOW_ROOT, 'templates', 'flows')
def list_flows():
    rv = []
    for filename in os.listdir(flow_templates_dir):
        rv.append(filename)
    rv.sort()
    return rv

@cli.command(short_help="Generate new flow based on a template")
@click.argument("template-name", required=False)
@click.argument("flow-name", required=False)
def generate(template_name, flow_name):
    """generates and opens new notebook NOTEBOOK_NAME,
    based on TEMPLATE_NAME"""

    if template_name is None:
        """If no arguments are provided, the CLI will display the list of
        existing flow templates.
        """

        click.echo("Usage: dsflow generate TEMPLATE_NAME FLOW_NAME...")
        show_instructions("\nChoose one of these templates:")
        for name in list_flows():
            show_instructions("    {}".format(name))

    else:
        """Templates are defined by template_specs.yaml and dag_specs.yaml

        Template generation works as follows:
        - create the flow directory
        - render dag_specs.yaml
        - read dag_specs.yaml and look for additional files to render
        - generate files related to each task
        - read template_specs.yaml
            - generate additional directories
            - print flow instructions

        """

        gen = DsflowGenerator()

        # Read template specs
        template_specs_path = os.path.join(DSFLOW_ROOT, "templates",
                                           "flows", template_name,
                                           "template_specs.yaml")

        template_specs = yaml.load(open(template_specs_path, 'r'))


        # Get template parameters
        user_template_parameters = dict()

        if "template_parameters" in template_specs:
            for parameter in template_specs["template_parameters"]:
                if parameter["type"] == "prompt":
                    user_template_parameters[parameter["name"]] = click.prompt(parameter["text"])

                if parameter["type"] == "confirm":
                    user_template_parameters[parameter["name"]] = click.confirm(parameter["text"])

        # Generate flow dir
        flow_dir = os.path.join(get_app_path(), 'flows', flow_name)
        gen.mkdir_and_log(flow_dir)

        t_parameters = dict(flow_name=flow_name,
                            ds=str(dt.date.today()),
                            **user_template_parameters)

        # genereate dag_specs.yaml

        template_path = os.path.join("flows", template_name, 'dag_specs.yaml.j2')
        dag_specs_w_path = os.path.join("flows", flow_name, 'dag_specs.yaml')

        gen.generate_file_from_template(template_path=template_path,
                                        target_path=dag_specs_w_path,
                                        **t_parameters)

        with open(os.path.join(get_app_path(), dag_specs_w_path), 'r') as f:
            # read dag_specs
            dag_specs = yaml.load(f)

        # Generate task files
        for (task_name, task_description) in dag_specs["tasks"].items():
            if "type" in task_description:
                # FIXME and task_description["type"] in ["py, sh, notebook"]

                task_type = task_description["type"]

                if "script" in task_description:
                    target_file_name = task_description["script"]
                else:
                    target_file_name = ".".join([task_name, task_type])

                # as a convention the template files use: task_name.task_type.j2
                task_template_file = ".".join([task_name, task_type, "j2"])
                task_template_path = os.path.join("flows", template_name, task_template_file)
                write_path = os.path.join("flows", flow_name, target_file_name)

                if task_type == "notebook":
                    """If the template is a notebook, then it has to be
                    generated based on the python file JOB_NAME.notebook.j2

                    Delimitate new cells with this syntax:

                        # <markdowncell>

                        # Initialize environment

                        # <codecell>

                        some_code()
                    """

                    t = gen.jinja_env.get_template(task_template_path)
                    contents = t.render(**t_parameters)

                    nb = nbf.v3.reads_py(contents)
                    nb = nbf.v4.upgrade(nb)

                    with open(write_path, "w") as outfile:
                        nbf.write(nb, outfile)

                    click.echo("     new file         %s" % write_path)

                else:
                    """Otherwise, simply render the file."""

                    gen.generate_file_from_template(template_path=task_template_path,
                                                    target_path=write_path,
                                                    **t_parameters)

        # Create new directories
        if "mkdir" in template_specs:
            for dir_path_template in template_specs["mkdir"]:
                dir_path = Template(dir_path_template) \
                  .render(**t_parameters) \
                  .replace("datastore:/", get_datastore_path())

                gen.mkdir_and_log(dir_path)

        # Print flow instructions
        if "instructions" in template_specs:
            click.echo("\nInstructions:")
            show_instructions(Template(template_specs["instructions"])
                              .render(flow_name=flow_name))
        else:
            show_instructions("\nInstructions:")
            show_instructions("Edit dag_specs")
            show_instructions("\n" % flow_name)


@cli.command(short_help="Run flow tasks")
@click.option("--ds", '-d', default=str(dt.date.today()))
@click.option("--task", "-t", required=False)
@click.argument("flow-name")
def run(flow_name, ds, task):
    """Run task in Docker

    Note: dsflow docker images must be running for this command to execute
    """
    client = docker.from_env()
    flow = Flow(flow_name)

    # If --task is not set, run everything
    if task:
        task_names = [task]
    else:
        task_names = flow.task_names

    # Task execution order follows "task_names" array order
    for task_instance_name in task_names:

        task_instance = flow.get_task_instance(task_instance_name, ds=ds)

        click.secho(dedent("""

                    ###########################################
                    Executing task
                    {flow_name} > {task_instance_name}
                    ###########################################
                    """.format(flow_name=flow_name,
                               task_instance_name=task_instance_name)), fg="green")
        click.secho(str(task_instance), fg="green")
        click.secho("")

        if task_instance["type"] == "sh":

            script_name = task_instance["script"]
            script_path = os.path.join(get_flows_path(), flow_name, script_name)

            if "source" in task_instance["parameters"] \
                and "sink" in task_instance["parameters"]:
                cmd = [script_path,
                       task_instance["parameters"]["source"],
                       task_instance["parameters"]["sink"]
                       ]
            else:
                cmd = [script_path]

            subprocess.call(["chmod", "+x", script_path])
            subprocess.call(cmd)


        if task_instance["type"] == "notebook":
            click.echo("Executing notebook")

            with click_spinner.spinner():
                input_path = "flows/%s/%s" % (flow_name, task_instance["script"])
                output_dir = "%s/flow_runs/%s/%s/" % (get_datastore_path(), flow_name, task_instance["ds"])
                output_dir_container = "/data/flow_runs/%s/%s" % (flow_name, task_instance["ds"])

                mkdir_if_needed(output_dir)

                docker_cmd = ("jupyter nbconvert --to html "
                              " --execute {} "
                              " --ExecutePreprocessor.allow_errors=True "
                              " --ExecutePreprocessor.timeout=3600 "
                              " --ExecutePreprocessor.kernel_name='python3'"
                              " --output-dir={}").format(input_path, output_dir_container)

                spark_container = client.containers.get("localdockerdefault_pyspark_1")

                output = spark_container.exec_run(docker_cmd)

                click.echo(output.decode("utf-8"))
                click.echo("View output at %s" % output_dir)
