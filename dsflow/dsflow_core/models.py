from IPython.display import display
from IPython.display import HTML, Markdown
import os
from pprint import *
import yaml
from textwrap import dedent
import datetime as dt
from jinja2 import Template

from .utils import get_datastore_path, get_flows_path


class Flow:
    def __init__(self, name):
        self.name = name
        self.flow_path = os.path.join(get_flows_path(), name)
        self.dag_specs_path = os.path.join(self.flow_path, "dag_specs.yaml")

        self.dag_specs = yaml.load(open(self.dag_specs_path, 'r'))
        self.task_names = self.dag_specs["pipeline"]


    def show(self):

        template = Template(dedent("""
        {{ description }}

        ## Tasks

        {% for k, v in tasks.items() %}
        - **{{ k }}**: {{ v.description }}
        {% endfor %}

        ## Datasets
        {% for k, v in datasets.items() %}
        - **{{ k }}**: {{ v.path }}
        {% endfor %}

        <p>Edit dag_specs.yaml to modify any of these properties.</p>


        """))

        return Markdown(template.render(self.dag_specs))

    def get_task_instance(self, task_name, ds="newest"):
        return TaskInstance(self.dag_specs, task_name, ds)

    def validate_dag_specs(self):
        pass


class TaskInstance(dict):
    def __getitem__(self, key):
        if key not in self:
            super(TaskInstance, self).__setitem__(key, [])
        return super(TaskInstance, self).__getitem__(key)

    def __init__(self, dag_specs, task_name, ds):
        self.dag_specs = dag_specs
        self.update(dag_specs["tasks"][task_name])
        self["name"] = task_name

        # populate default values
        if "script" not in self:
            self["script"] = "%s.%s" % (self["name"], self["type"])

        if ds == "today":
            self["ds"] = "ds=%s" % str(dt.date.today())

        elif ds == "newest":
            if "parameters" in self and "source" in self["parameters"]:
                source_name = self["parameters"]["source"]
                source_base_path = self.dag_specs["datasets"][source_name]["path"].replace("datastore:", get_datastore_path())

                self["ds"] = max(os.listdir(source_base_path))
            else:
                raise Exception("ds can't be set to 'newest' if no source dataset is specified")
        else:
            self["ds"] = "ds=%s" % ds

        # render parameters
        if "parameters" in self:
            # if a parameter refers to a dataset, then it should be replaced
            params = self["parameters"]
            self["original_parameters"] = params.copy()

            dataset_names = self.dag_specs["datasets"].keys()

            for (param_name, param_value) in params.items():
                if param_value in dataset_names:
                    # replace dataset name by dataset specs
                    params[param_name] = self.dag_specs["datasets"][param_value]

                    # update datastore path
                    dataset_base_path = params[param_name]["path"].replace("datastore:", get_datastore_path())

                    params[param_name] = os.path.join(dataset_base_path, "%s" % self["ds"])

        self.ds = self["ds"]

    def show(self):
        pprint(dict(**self))

    def __repr__(self):
        return pformat(dict(**self))

    def ds_read_path(self):
        return self["parameters"]["source"]

    def ds_write_path(self):
        return self["parameters"]["sink"]
