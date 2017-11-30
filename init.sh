# Is Docker running?
if [[ $(docker version --format "{{.Server.KernelVersion}}") == *-moby ]]; then

  # exporting env. variables
  export DSFLOW_WORKSPACE=$(pwd)
  export DSFLOW_ROOT=$(pwd)/dsflow

  # create docker network
  echo ""
  echo "=== creating docker network \"dsflow\"..."
  docker network create dsflow

  # exporting dsflow
  alias dsflow='function _dsflow(){ if [[ -z "$1" ]]; then python $DSFLOW_ROOT/dsflow-menu.py; else python $DSFLOW_ROOT/dsflow-$1.py "${@:2}"; fi; };_dsflow'

  # prompt user about docker images
  echo ""
  read -p "=== would you like to download and build docker images? [y/N]" -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
      dsflow build-images
  fi

  # Display message:
  echo ""
  echo ""
  echo "=================== IMPORTANT ============================================"
  echo "you need to execute \`source init.sh\` every time you open a new terminal!"
  echo ""
  echo "HINT: display the list of available commands using"
  echo "$ dsflow"
  echo "=========================================================================="


else
  echo "=================== ERROR ========================="
  echo "Docker is not running. Please open the app, or run:"
  echo "$ open --background -a Docker"
  echo "Then wait a few seconds an rety."
  echo "==================================================="
fi
