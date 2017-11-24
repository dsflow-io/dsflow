# install python libraries
if hash pip 2>/dev/null; then
    pip install pyyaml
elif hash pip3 2>/dev/null; then
    pip3 install pyyaml
else
    echo "pip not found. Please install Python."
fi

# create dsflow docker network
docker network create dsflow

# exporting env. variables
export DSFLOW_WORKSPACE=$(pwd)
export DSFLOW_ROOT=$(pwd)/dsflow

# exporting dsflow
alias dsflow='function _dsflow(){ if [[ -z "$1" ]]; then python $DSFLOW_ROOT/dsflow-menu.py; else python $DSFLOW_ROOT/dsflow-$1.py "${@:2}"; fi; };_dsflow'

# prompt user about docker images
read -p "Would you like to download and build docker images? [y/N]" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    dsflow build-images
fi
