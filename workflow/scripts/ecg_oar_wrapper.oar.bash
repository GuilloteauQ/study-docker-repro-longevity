#!/bin/bash

set -xe

DIRECTORY=$1
shift
BUILD_STATUS_FILE=$1
shift
ARTIFACT_FILE=$1
shift

# To "activate" nix on the node
export PATH=~/.local/bin:$PATH

# Install Docker on the node (-t is to store the images on /tmp because it has more disk)
# https://www.grid5000.fr/w/Docker
g5k-setup-docker -t

handler() {
    echo "${ARTIFACT_FILE}, `date +%s.%N`, job_time_exceeded" >> ${BUILD_STATUS_FILE}; exit 0;
}
trap handler SIGUSR2

cd ${DIRECTORY}
nix develop --command $@
