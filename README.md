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
dsflow generate-notebook from_csv TABLE_NAME

```
