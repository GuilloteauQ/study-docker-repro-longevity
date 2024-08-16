#!/bin/bash

ANALYSIS_TYPE=$1
OUTPUT=$2
shift; shift

ARGS=$@
INPUT=("${ARGS[@]/#/-i }")
SCRIPT=""
OPT=""

case ANALYSIS_TYPE in
    "softenv")
        SCRIPT="softenv_analysis.py"
        OPT="-t sources-stats"
    ;;

python3 softenv_analysis.py -t sources-stats $INPUT -o