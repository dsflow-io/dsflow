FROM jupyter/pyspark-notebook

RUN pip install httpie

RUN pip install plotnine

RUN pip install pyyaml

WORKDIR /usr/src/app

# ADD docker/dsflow-schema-generator /usr/src/app

CMD "python dsflow_core/infer_schema.py"
