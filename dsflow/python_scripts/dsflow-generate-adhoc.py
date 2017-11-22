import os
import sys
import subprocess
from dsflow_core.utils import *
from dsflow_core.models import *

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]

flow_templates_dir = os.path.join(DSFLOW_ROOT, 'templates', 'jobs')
def list_jobs():
    rv = []
    for filename in os.listdir(flow_templates_dir):
        rv.append(filename)
    rv.sort()
    return rv


def generate(dataset_type, dataset_name, source_path, schema_path):

    gen = DsflowGenerator()

    t_parameters = dict(ds=str(dt.date.today()),
                        dataset_type=dataset_type,
                        dataset_name=dataset_name,
                        source_path=source_path,
                        schema_path=schema_path)


    target_file_name = "%s-explore-%s.ipynb" % (str(dt.date.today()), dataset_name)
    write_path = os.path.join("/adhoc", target_file_name)

    # as a convention the template files use: job_name.job_class.j2
    task_template_file = ".".join([dataset_type, "py", "j2"])
    task_template_path = os.path.join("adhoc", task_template_file)

    """If the template is a notebook, then it has to be
    generated based on the python file dataset_type.py.j2

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


generate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
