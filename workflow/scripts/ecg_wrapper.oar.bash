#!/bin/bash

set -xe

# To "activate" nix on the node
export PATH=~/.local/bin:$PATH

# Install Docker on the node (-t is to store the images on /tmp because it has more disk)
# https://www.grid5000.fr/w/Docker
g5k-setup-docker -t

handler() {
    echo "Caught checkpoint signal at: `date`"; echo "Terminating."; exit 0;
}
trap handler SIGUSR2

nix develop --command $@
