alias dsflow='function _dsflow(){ if [[ -z "$1" ]]; then python dsflow/dsflow-menu.py; else python dsflow/dsflow-$1.py "${@:2}"; fi; };_dsflow'
