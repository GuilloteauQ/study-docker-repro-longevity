#!/bin/python3

"""
    ECG is program that automates software environment checking
    in scientific artifacts.

    It is meant to be executed periodically to analyze variations in the
    software environment of the artifact through time.
"""

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
import logging

# Paths:
HEREPATH = pathlib.Path(__file__).parent.absolute()
# Where to store list of installed packages:
PKGLISTS = "./pkglists/"

# Commands to list installed packages along with their versions and the name
# of the package manager, depending on the package managers.
# Each package manager is associated with a tuple, the first item being
# the query command, and the second being the command that will format
# the output of the query command (this one can be an empty string in case
# the formatting part is already done using the options of the first command).
# The first needs to be run on the container, and the second on the host,
# to take into account container images that do not have the formatting
# packages installed.
pkgmgr_cmd = {
    "dpkg": ("dpkg -l", "awk 'NR>5 {print $2 \",\" $3 \",\" \"dpkg\"}'"), \
    "rpm":("rpm -qa --queryformat '%{NAME},%{VERSION},rpm\\n'", ""), \
    "pacman":("pacman -Q", "awk '{print $0 \",\" $1 \",pacman\"}'"), \
    "pip":("pip freeze", "sed 's/==/,/g' | awk '{print $0 \",pip\"}'"), \
    "conda":("/root/.conda/bin/conda list -e", "sed 's/=/ /g' | awk 'NR>3 {print $1 \",\" $2 \",conda\"}'")
}

# Command to obtain the latest commit hash in a git repository:
gitcmd = "git log -n 1 --pretty=format:%H"

# Enables logging:
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def download_sources(config):
    """
        Downloads the source of the artifact in 'config'.

        Parameters
        ----------
        config: dict
            Parsed YAML config file.

        Returns
        -------
        temp_dir: tempfile.TemporaryDirectory
            The directory where the artifact is downloaded to.
    """
    url = config["artifact_url"]
    logging.info(f"Downloading artifact from {url}")
    temp_dir = tempfile.TemporaryDirectory()
    req = requests.get(url)
    if config["type"] == "zip":
        artifact = zipfile.ZipFile(io.BytesIO(req.content))
    elif config["type"] == "tgz":
        artifact = tarfile.open(fileobj=io.BytesIO(req.content))
    logging.info(f"Extracting artifact at {temp_dir.name}")
    artifact.extractall(temp_dir.name)
    return temp_dir

def build_image(config, src_dir):
    """
        Builds the given Docker image in 'config'.

        Parameters
        ----------
        config: dict
            Part of the parsed YAML config file concerning the Docker image
            to build.

        src_dir: tempfile.TemporaryDirectory
            The directory where the artifact is stored.

        Returns
        -------
        return_code: int
            Return code of the Docker 'build' command.
    """
    name = config["name"]
    logging.info(f"Starting building image {name}")
    path = os.path.join(src_dir, config["location"])
    build_command = "docker build -t " + config["name"] + " ."
    # subprocess.check_call(config["build_command"].split(" "), cwd=path)
    build_process = subprocess.run(build_command.split(" "), cwd=path, capture_output=False)
    return_code = build_process.returncode
    logging.info(f"Command '{build_command}' exited with code {return_code}")
    return return_code == 0

def check_env(config, src_dir):
    """
        Builds a list of all software packages installed in the
        Docker image given in 'config', depending on the package managers
        specified in the configuration, then stores it in a CSV file.

        Parameters
        ----------
        config: dict
            Part of the parsed YAML config file concerning the Docker image
            where to check the environment.

        src_dir: tempfile.TemporaryDirectory
            The directory where the artifact is stored.

        Returns
        -------
        None
    """
    pathlib.Path(PKGLISTS).mkdir(parents=True, exist_ok=True)
    pkglist_file = open(PKGLISTS + "pkglist.csv", "w")
    pkglist_file.write("Package,Version,Package manager\n")
    path = os.path.join(src_dir, config["location"])
    for pkgmgr in config["package_managers"]:
        logging.info(f"Checking '{pkgmgr}'")
        pkglist_process = subprocess.run(["docker", "run", "--rm", config["name"]] + pkgmgr_cmd[pkgmgr][0].split(" "), cwd=path, capture_output=True)
        format_process = subprocess.run("cat << EOF | " + pkgmgr_cmd[pkgmgr][1] + "\n" + pkglist_process.stdout.decode("utf-8") + "EOF", cwd=path, capture_output=True, shell=True)
        pkglist = format_process.stdout.decode("utf-8")
        pkglist_file.write(pkglist)
    if "git_packages" in config.keys():
        logging.info("Checking Git packages")
        for repo in config["git_packages"]:
            pkglist_process = subprocess.run(["docker", "run", "--rm", "-w", repo["location"], config["name"]] + gitcmd.split(" "), cwd=path, capture_output=True)
            repo_row = repo["name"] + "," + pkglist_process.stdout.decode("utf-8") + ",git"
            pkglist_file.write(repo_row + "\n")
    if "misc_packages" in config.keys():
        logging.info("Checking packages obtained outside of a package manager or VCS")
        for pkg in config["misc_packages"]:
            logging.info(f"Downloading package {pkg["name"]} from {pkg["url"]}")
            req = requests.get(pkg["url"])
            pkg_file = tempfile.NamedTemporaryFile()
            pkg_file.write(req.content)
            pkglist_process = subprocess.run("sha256sum " + pkg_file.name + " | cut -zd ' ' -f 1", cwd=path, capture_output=True, shell=True)
            pkg_row = pkg["name"] + "," + pkglist_process.stdout.decode("utf-8") + ",misc"
            pkglist_file.write(pkg_row + "\n")
    pkglist_file.close()

def remove_image(config):
    """
        Removes the Docker image given in 'config'.

        Parameters
        ----------
        config: dict
            Part of the parsed YAML config file concerning the Docker image
            to remove.

        Returns
        -------
        None
    """
    name = config["name"]
    logging.info(f"Removing image '{name}'")
    subprocess.run(["docker", "rmi", name])

def build_images(config, src_dir):
    """
        Builds all Docker images specified in 'config', checks software
        environment if build is successful, then removes the images.

        Parameters
        ----------
        config: dict
            Parsed YAML config file.

        src_dir: tempfile.TemporaryDirectory
            The directory where the artifact is stored.

        Returns
        -------
        None
    """
    for image in config["dockerfiles"]:
        successful_build = build_image(image, src_dir)
        if successful_build:
            check_env(image, src_dir)
            remove_image(image)

def main():
    # Command line arguments parser:
    parser = argparse.ArgumentParser(
                    prog='ecg',
                    description='Check if a dockerfile is still buildable')
    parser.add_argument('config')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    # Parsing the input YAML file including the configuration of the artifact:
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
