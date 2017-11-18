FROM python:3

# RUN mkdir -p .jupyter/migrated/

# USER root

# USER $NB_USER

#ENV SPARK_CONF_DIR=/home/jovyan/
#ENV PYSPARK_DRIVER_PYTHON="jupyter"
#ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook"

RUN pip install configparser && \
    pip install Click==6.7 && \
    pip install nbformat==4.4 && \
    pip install pyyaml==3.12 && \
    pip install "Jinja2<2.9.0,>=2.7.3" && \
    pip install xlwt==1.3 && \
    pip install requests && \
    pip install IPython && \
    pip install click-spinner && \
    pip install envparse==0.2.0

ADD dsflow-core-lib/dsflow /usr/src/app/dsflow
ADD templates /usr/src/app/templates

# RUN pip install -e /usr/src/app/dsflow

WORKDIR /usr/src/app

ADD docker/dsflow-notebook-generator /usr/src/app

# EXPOSE 8888

# ENV NAME Dsflow

CMD "python dsflow-generate-notebook.py"
