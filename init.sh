export DSFLOW_WORKSPACE=$(pwd)
export DSFLOW_ROOT=$(pwd)/dsflow

alias dsflow='function _dsflow(){ if [[ -z "$1" ]]; then python $DSFLOW_ROOT/dsflow-menu.py; else python $DSFLOW_ROOT/dsflow-$1.py "${@:2}"; fi; };_dsflow'

read -p "Would you like to download and build docker images? [y/N]" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    dsflow build-images
fi
