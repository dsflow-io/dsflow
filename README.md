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


### [optional] install and use dsflow within a virtual environment:

```
pip install virtualenv
virtualenv ~/.venv-dsflow
source ~/.venv-dsflow/bin/activate

```


### New dsflow project:

- Normally with `dsflow new PROJECT_NAME`
- Alternative: just duplicate this directory


### Execute a notebook:

```
python dsflow/dsflow-run.py jobs/table-people/create.ipynb 2017-11-09


```

### Launch notebook environment:

```
python dsflow/dsflow-start-notebook.py

```


### Generate table from CSV

```
python dsflow/dsflow-generate-notebook.py from_csv

```
