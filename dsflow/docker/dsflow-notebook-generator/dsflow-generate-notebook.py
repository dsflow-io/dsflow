import click
import os
from dsflow.utils import *
from dsflow.models import *

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]

flow_templates_dir = os.path.join(DSFLOW_ROOT, 'templates', 'jobs')
def list_jobs():
    rv = []
    for filename in os.listdir(flow_templates_dir):
        rv.append(filename)
    rv.sort()
    return rv


@click.command(short_help="Generate new flow based on a template")
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
        for name in list_jobs():
            show_instructions("    {}".format(name))

    else:
        """Templates are defined by template_specs.yaml and dag_specs.yaml

        Template generation works as follows:
        - create the jobs directory
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
                                           "jobs", template_name,
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

        # Generate jobs dir
        jobs_dir = os.path.join(get_jobs_path(), flow_name)
        gen.mkdir_and_log(jobs_dir)

        t_parameters = dict(flow_name=flow_name,
                            ds=str(dt.date.today()),
                            **user_template_parameters)

        # genereate dag_specs.yaml

        template_path = os.path.join("jobs", template_name, 'dag_specs.yaml.j2')
        dag_specs_w_path = os.path.join(get_jobs_path(), flow_name, 'dag_specs.yaml')

        gen.generate_file_from_template(template_path=template_path,
                                        target_path=dag_specs_w_path,
                                        **t_parameters)

        with open(os.path.join(dag_specs_w_path), 'r') as f:
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
                task_template_path = os.path.join("jobs", template_name, task_template_file)
                write_path = os.path.join(get_jobs_path(), flow_name, target_file_name)

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


if __name__ == '__main__':
    generate()
