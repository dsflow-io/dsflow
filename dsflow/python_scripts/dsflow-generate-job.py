import os
import sys
import subprocess
from dsflow_core.utils import *

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]

flow_templates_dir = os.path.join(DSFLOW_ROOT, 'templates', 'jobs')
def list_jobs():
    rv = []
    for filename in os.listdir(flow_templates_dir):
        rv.append(filename)
    rv.sort()
    return rv


def generate(template_name, dataset_name):
    """generates and opens new job,
    based on TEMPLATE_NAME"""

    if template_name is None:
        """If no arguments are provided, the CLI will display the list of
        existing flow templates.
        """

        print("Usage: dsflow generate-job TEMPLATE_NAME JOB_NAME...")
        show_instructions("\nChoose one of these templates:")
        for name in list_jobs():
            show_instructions("    {}".format(name))

        show_instructions("\nIf this is the first job your create, "
                          "we suggest your start with `download_file`:"
                          "\n\nFor instance:"
                          "\n$ dsflow generate-job download_file my_dataset_name")

    else:
        """Templates are defined by template_specs.yaml and job_specs.yaml

        Template generation works as follows:
        - create the jobs directory
        - render job_specs.yaml
        - read job_specs.yaml and look for additional files to render
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

        job_name_prefix = template_specs["job_name_prefix"]
        job_name = job_name_prefix + "-" + dataset_name

        # Generate jobs dir
        jobs_dir = os.path.join(get_jobs_path(), job_name)
        gen.mkdir_and_log(jobs_dir)

        t_parameters = dict(job_name=job_name,
                            dataset_name=dataset_name,
                            ds=str(dt.date.today()),
                            **user_template_parameters)

        # genereate job_specs.yaml

        template_path = os.path.join("jobs", template_name, 'job_specs.yaml.j2')
        job_specs_w_path = os.path.join(get_jobs_path(), job_name, 'job_specs.yaml')

        gen.generate_file_from_template(template_path=template_path,
                                        target_path=job_specs_w_path,
                                        **t_parameters)

        with open(os.path.join(job_specs_w_path), 'r') as f:
            # read job_specs
            job_specs = yaml.load(f)


        if "class" in job_specs:
            # FIXME check that class is valid

            job_class = job_specs["class"]
            target_file_name = job_specs["script"]
            write_path = os.path.join(get_jobs_path(), job_name, target_file_name)

            if job_class == "JupyterNotebook":
                # as a convention the template files use: job_name.job_class.j2
                task_template_file = ".".join(["notebook", "py", "j2"])
                task_template_path = os.path.join("jobs", template_name, task_template_file)

                """If the template is a notebook, then it has to be
                generated based on the python file notebook.py.j2

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

                print("     new file         %s" % write_path)

            elif job_class == "CommandLineTool":
                """Otherwise, simply render the file."""
                task_template_file = ".".join(["script", "sh", "j2"])
                task_template_path = os.path.join("jobs", template_name, task_template_file)

                gen.generate_file_from_template(template_path=task_template_path,
                                                target_path=write_path,
                                                **t_parameters)

                subprocess.call(["chmod", "+x", write_path])


            elif job_class == "PlotlyDashApplication":
                    """Otherwise, simply render the file."""
                    task_template_file = ".".join(["dashboard", "py", "j2"])
                    task_template_path = os.path.join("jobs", template_name, task_template_file)

                    gen.generate_file_from_template(template_path=task_template_path,
                                                    target_path=write_path,
                                                    **t_parameters)

            else:
                raise(Exception("Unsupported job class"))


            # render README
            readme_template_path = os.path.join("jobs", template_name, 'README.md.j2')
            readme_target_path = os.path.join(get_jobs_path(), job_name, 'README.md')
            gen.generate_file_from_template(template_path=readme_template_path,
                                            target_path=readme_target_path,
                                            **t_parameters)

        else:
            raise(Exception("invalid job_specs.yaml (missing class property)"))

        # Create new directories
        if "mkdir" in template_specs:
            for dir_path_template in template_specs["mkdir"]:
                dir_path = Template(dir_path_template) \
                  .render(**t_parameters) \
                  .replace("datastore:/", get_datastore_path())

                gen.mkdir_and_log(dir_path)

        # Print flow instructions (FIXME!)
        print("\nInstructions:")
        show_instructions(open(readme_target_path, 'r').read())


generate(sys.argv[1] if len(sys.argv) > 1 else None, sys.argv[2] if len(sys.argv) > 2 else None)
