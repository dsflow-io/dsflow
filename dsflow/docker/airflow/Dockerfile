FROM puckel/docker-airflow:1.8.2

USER root

# Install Docker from Docker Inc. repositories.
RUN curl -sSL https://get.docker.com/ | sh

RUN pip install docker-compose

RUN gpasswd -a airflow docker

# USER airflow

WORKDIR /root/
