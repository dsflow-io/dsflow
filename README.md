# dsflow v-0.3.1

![dsflow logo](docs/src/dsflow-logo.png?raw=true "dsflow")

_IMPORTANT: this is an early release of dsflow, designed for prototyping of data pipeline on your own computer._


## What is dsflow?

We're pleased to introduce _dsflow_ — the **framework for data science**.

_Dsflow_ helps you build powerful and flexible **pipelines for data analytics**.
The current version is designed for use on your local computer, using the **command line interface**.
Eventually you'll be able to use dsflow to deploy your pipelines to cloud platforms.

Interested? Subscribe to our mailing list on [dsflow.io](http://dsflow.io)

## Quick start / main features

- install or update Docker 🐳 (`brew cask install docker`)
- clone this repo
- execute `source init.sh` to initialize the environment and build docker images (_it might take over 10 minutes to download all sources_ ☕️)
- execute `dsflow` to see the list of commands
- execute `dsflow generate-job`: display the list of job templates
- execute `dsflow generate-job TEMPLATE_NAME JOB_NAME`: generate a job based on a template
- execute `dsflow run JOB_NAME`: runs the job in its associated container
- execute `dsflow start-jupyter` to open the default IDE in your browser (Jupyter Lab with pyspark) at http://localhost:8888/
- execute `dsflow stop-all` to terminate all dsflow Docker containers.

See documentation below for detailed instructions.


## Dsflow tech stack 360

These are the default technologies when using dsflow:

- Run everything within containers  (using [Docker](https://www.docker.com/what-docker)).
- Query and transform data with [Apache Spark 2.2](https://spark.apache.org/).
- Store data as [Parquet files](https://parquet.apache.org/).
- Write code and iterate on your scripts using [Jupyter](http://jupyter.org/).
- Orchestrate your jobs and pipelines with [Apache Airflow (incubating)](https://airflow.apache.org/) – _not implemented yet_.
- Build powerful dashboards with [Plotly Dash](https://plot.ly/dash/).
- Collaborate with your team using Github (or any [version control systems](https://en.wikipedia.org/wiki/Version_control)).


## Dsflow core principles

**Note**: if you're not familiar with these principles, dsflow CLI and job templates will help you adopt them.


### Separation of compute and storage

Unlike traditional databases, dsflow relies on the principle of separation of compute and storage.

When you run dsflow on your computer, your resources -- **data**, jobs, notebooks, docker files -- are stored in distinct directories. It's organized in a way that simplifies deployment of your pipelines to the cloud.

**Data** is stored in a directory called `datastore/`:

- as such you could use any Big Data compute engine (Spark, Hive, Presto, etc.) to query it.
- this `datastore/` directory can be local or distant
- \[future release\]: dsflow will help you download samples of your production datastore, so that it gets easier to iterate locally on smaller datasets.
- \[future release\]: dsflow will help manage multiple datastores, in order to provide access control and better resources management.

**Scripts** are stored in a directory called `jobs/`:

- they are distinct from the data they process.
- all jobs MUST take **input** and **output** parameters (or **source** / **sink** parameters), because the logic has to be independent from what it processes.  
For instance, you should be able to run the same script on local data and on distant data.

### Containers

Running your data transformations (jobs) within Docker containers bring many advantages:

- **No more library conflicts**  
Big data tools and ML libraries keep evolving. Being able to run each script in an isolated environment is critical in order to avoid conflicts, and run both legacy script and cutting edge logic.
- **Easily adopt newest Data Science tools**  
New software won't impact legacy tools.
- **Portability**  
Run a script on your laptop or in the cloud seamlessly. Stay independent from your cloud provider.
- **Scalability**  
Each task (instance of a job) runs in its own container. It allows a better allocation of resources: running tasks in parallel, using a memory configuration optimized for each task.


### Daily partitions of data

`ds` is not only the initials of Data Science, it's also the default name for date partitions.

When you store your data with daily partitions, you get immediately the following benefits:

- versioning of your data
- keeping daily snapshots of a dataset makes it easier to compute KPIs and monitor the evolution of the
- you avoid overwriting data, instead you append by creating a new partition
- it's an efficient way to store large datasets
- it makes it easier to optimize queries of large datasets, by selecting the `ds` range that matters.



## Documentation

### Requirements

Brew and Python need to be installed on your system.
If not, execute in your terminal:

```
xcode-select --install
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python
```

A recent version of Docker is needed:

```
brew cask install docker
```

Installation on Ubuntu: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/


**Frequent issues when installing dsflow on macOS**

- xcode: If your it is outdated, update it with the app store, or just move it to Trash.
- Python: dsflow CLI works with Python 2.7 and 3.3+ and only requires the `pyyaml` module in addition to core modules. Scripts with additional requirements will run in containers.
- Docker: make sure it's running before launching dsflow.
- Docker-compose: make sure it's up-to-date (dsflow requires support for version '3.3')




### Initialize dsflow

Inside the dsflow project directory:

```
source init.sh

```

**In depth:**

This will set up environment variables and provide a shortcut to dsflow commands.  
For instance, `dsflow tree` will execute `python dsflow/dsflow-tree.py`


### Show list of available commands

```
dsflow
```


### Quickly download and explore dataset

run `dsflow generate-adhoc NOTEBOOK_NAME DATASET_URL csv|json`: dsflow will generate a notebook `NOTEBOOK_NAME` and will help you explore a csv or json dataset.


JSON files:

```
dsflow generate-adhoc meteo_paris "https://data.opendatasoft.com/explore/dataset/prevision-meteo-paris-arome@paris-saclay/download/?format=json&timezone=Europe/Berlin" json
```

CSV files:

```
dsflow generate-adhoc meteo_france "https://data.opendatasoft.com/explore/dataset/donnees-synop-agregees-journalier@api-agro/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true" csv
```

Notes:

- make sure URL is quoted with \"



### Execute a notebook:

```
dsflow run JOB_NAME PARAMETERS
dsflow run meteo-json-dump 2017-11-09
dsflow run meteo-create-table 2017-11-09

```

### Launch notebook environment:

```
dsflow start-notebook

```


### Generate table from CSV

```
dsflow generate-job create_table_from_csv TABLE_NAME

```

## FAQ

### Is dsflow available on Windows?

dsflow hasn't been tested on Windows yet.

We recommend the use of [Windows 10 linux shell](https://msdn.microsoft.com/en-us/commandline/wsl/install-win10).

Install Docker on Windows:
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/
