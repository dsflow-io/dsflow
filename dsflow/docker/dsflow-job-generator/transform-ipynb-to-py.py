import os
import sys
from dsflow_core.utils import *
from dsflow_core.models import *

DSFLOW_ROOT = os.environ["DSFLOW_ROOT"]


def transform(notebook_name):
    """Convert notebook NOTEBOOK_NAME into a task.
    WARNING!
    Currently, it only converts the notebook into a Python file,
    but does not create the task.
    """

    input_file = '/jobs/%s.ipynb' % notebook_name
    output_file = '/jobs/%s.py' % notebook_name
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


transform(sys.argv[1])
