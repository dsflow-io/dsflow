# dsflow v-0.3.1

~~ DISCLAIMER: dsflow is being developed, and its APIs are not stable ~~


## What is dsflow?

We're pleased to introduce _dsflow_ — the framework for data scientists!

_Dsflow_ helps you build powerful and flexible **pipelines for data analytics**.
The current version is designed for use on your local computer, using the **command line interface**.
Eventually you'll be able to use dsflow to deploy your pipelines to popular cloud providers.

Subscribe on our website: http://dsflow.io

## Quick start

- install and launch Docker 🐳 (`brew cask install docker`)
- clone this repo
- execute `source init.sh` to initialize the environment and build docker images (_it might take over 10 minutes to download all sources_ ☕️)
- run `dsflow` to see the list of commands
- run `dsflow start-notebook` to open the default IDE in your browser (Jupyter Lab with pyspark)
- run `dsflow generate-adhoc NAME DATASET_URL csv|json`: dsflow will generate a notebook `NAME` and will help you explore a csv or json dataset.
- run `dsflow stop-all` to terminate all dsflow Docker containers.

See below for detailed instructions.


## Dsflow facts

- Container technology (Docker) is at the core of dsflow.
- Apache Spark 2.2+ is the default compute engine.
- Jupyter notebooks are the default environment for data science.
- Apache Airflow (incubating) is the default job orchestrator
- all resources created by dsflow are stored on the filesystem.


## Use cases

### Create a dashboard to track correlations between weather and search trends




## Documention


### Requirements:

Python 3 and Docker (a recent version -- October 2017) need to be installed on your system.
If not, execute in your terminal:

```
xcode-select --install
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew cask install docker
brew install python
```

Installation on Ubuntu: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/


### dsflow on Windows?

dsflow hasn't been tested on Windows yet.

We recommend the use of [Windows 10 linux shell](https://msdn.microsoft.com/en-us/commandline/wsl/install-win10).

Install Docker on Windows:
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/


### Initialize dsflow

Inside the dsflow project directory:

```
source init.sh

```

**In depth:**

This will set up environment variables and provide a shortcut to dsflow commands.  
For instance, `dsflow tree` will execute `python dsflow/dsflow-root.py`

### Show list of available commands

```
dsflow

```


### Download and explore dataset

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
