#!/bin/python3

import subprocess
import json
import yaml
import argparse
import tempfile
import os
import requests
import zipfile
import io
import tarfile

import pathlib
HEREPATH = pathlib.Path(__file__).parent.absolute()

# Where to store list of installed packages:
PKGLISTS = "./pkglists/"

# Commands to list installed packages along with their versions and the name of the package manager, depending on the packages manager:
pkgmgr_cmd = {"dpkg":"dpkg -l | awk 'NR>5 {print $2 \",\" $3 \",\" \"dpkg\"}'", "rpm":"rpm -qa --queryformat '%{NAME},%{VERSION},rpm\\n'", "pacman":"pacman -Q | awk '{print $0 \",\" $1 \",pacman\"}'", "pip":"pip freeze | sed 's/==/,/g' | awk '{print $0 \",pip\"}'", "conda":"/root/.conda/bin/conda list"}

import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def download_sources(config):
    url = config["artifact_url"]
    logging.info(f"Downloading sources from {url}")
    temp_dir = tempfile.TemporaryDirectory()
    req = requests.get(url)
    if config["type"] == "zip":
        artefact = zipfile.ZipFile(io.BytesIO(req.content))
    elif config["type"] == "tgz":
        artefact = tarfile.open(fileobj=io.BytesIO(req.content))
    artefact.extractall(temp_dir.name)
    logging.info(f"Extracting sources at {temp_dir.name}")
    return temp_dir

def build_image(config, src_dir):
    name = config["name"]
    logging.info(f"Starting building image {name}")
    path = os.path.join(src_dir, config["location"])
    build_command = "docker build -t " + config["name"] + " ."
    # subprocess.check_call(config["build_command"].split(" "), cwd=path)
    build_process = subprocess.run(build_command.split(" "), cwd=path, capture_output=True)
    return_code = build_process.returncode
    stderr = build_process.stderr
    logging.info(f"Command {build_command} exited with code {return_code} ({stderr})")
    return return_code == 0

def check_env(config, src_dir):
    pathlib.Path(PKGLISTS).mkdir(parents=True, exist_ok=True)
    path = os.path.join(src_dir, config["location"])
    pkglist_file = open(PKGLISTS + "pkglist.csv", "w")
    pkglist_file.write("Package,Version,Package manager\n")
    for pkgmgr in config["package_managers"]:
        logging.info(f"Checking '{pkgmgr}'")
        check_process = subprocess.run("docker run --rm " + config["name"] + " " + pkgmgr_cmd[pkgmgr], cwd=path, capture_output=True, shell=True)
        pkglist = check_process.stdout.decode("utf-8")
        print(pkglist)
        pkglist_file.write(pkglist)
    pkglist_file.close()

def remove_image(config):
    name = config["name"]
    logging.info(f"Removing image '{name}'")
    subprocess.run(["docker", "rmi", name])

def build_images(config, src_dir):
    for image in config["dockerfiles"]:
        successful_build = build_image(image, src_dir)
        if successful_build:
            check_env(image, src_dir)
            remove_image(image)

def main():
    parser = argparse.ArgumentParser(
                    prog='ecg',
                    description='Check if a dockerfile is still buildable')
    parser.add_argument('config')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()
    config = None
    with open(args.config, "r") as config_file:
        config = yaml.safe_load(config_file)
    verbose = args.verbose

    # if verbose:
    #    logging.info(f"Output will be stored in {output}")

    src_dir = download_sources(config)
    build_images(config, src_dir.name)
    return 0

if __name__ == "__main__":
    main()
