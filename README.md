# dsflow v-0.3 alt

### Requirements:

Brew, Python and Docker need to be installed on your system.
If not, execute in your terminal:

```
xcode-select --install
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew cask install docker
brew install python
```

Installation on Ubuntu: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/

Installation on Windows:
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/


### Initialize dsflow

Inside the dsflow project directory:

```
source init.sh

```


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
