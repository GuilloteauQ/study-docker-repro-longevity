#!/bin/python3

"""
    ECG is a program that automates software environment checking
    for scientific artifacts.

    It is meant to be executed periodically to analyze variations in the
    software environment of the artifact through time.
"""

import subprocess
import json
import argparse
import tempfile
import os
import requests
import zipfile
import tarfile
import pathlib
import logging
import datetime
import sys
import string
import traceback
import hashlib

def download_file_and_get_hash(url, dest_path):
    file_hash = "-1"
    try:
        req = requests.get(url)
        if req.status_code != 404:
            with open(dest_path, "wb") a file:
                file.write(req.content)
            file_hash = hashlib.sha256(req.content).hexdigest()
    except requests.exceptions.ConnectionError:
        # We can just ignore this exception, as we will just return an empty
        # hash to indicate the error:
        pass
    return file_hash

def download_sources(url, archive_type, arthashlog_path, dl_dir, artifact_name):
    logging.info(f"Downloading artifact from {url}")

    artifact_dir = ""

    tmp_artifact_file = tempfile.NamedTemporaryFile()
    tmp_artifact_path = artifact_file.name
    artifact_hash = download_file_and_get_hash(url, tmp_artifact_path)

    if artifact_hash != "-1":
        logging.info(f"Extracting artifact at {artifact_dir}")
        artcache_dir = f"ecg_{artifact_hash[:9]}"
        artifact_dir = os.path.join(dl_dir, artcache_dir)
        extractors = {
            "zip": zipfile.ZipFile,
            "tar": tarfile.open
        }
        os.mkdir(artifact_dir)
        extractors[archive_type](artifact_path).extractall(artifact_dir)

    with open(arthashlog_path, "w") as arthashlog_file:
        now = datetime.datetime.now()
        timestamp = str(datetime.datetime.timestamp(now))
        arthashlog_file.write(f"{timestamp},{artifact_hash},{artifact_name}\n")

    return artifact_dir

def builderror_identifier(output):
    build_errors = {
        "package_install_failed": ("Unable to locate package", "error: failed to compile"),
        "baseimage_unavailable": ("manifest unknown: manifest unknown",),
        "dockerfile_not_found": ("Dockerfile: no such file or directory",)
    }
    for error_cat, error_msgs in build_errors.items():
        for error in error_msgs:
            if error in output:
                return error_cat
    return "unknown_error"

def buildresult_saver(result, buildstatus_path, config_path):
    with open(buildstatus_path, "w") as buildstatus_file:
        artifact_name = os.path.basename(config_path).split(".")[0]
        now = datetime.datetime.now()
        timestamp = str(datetime.datetime.timestamp(now))
        buildstatus_file.write(f"{artifact_name},{timestamp},{result}\n")

def build_image(path, image_name):
    logging.info(f"Starting building image {image_name}")
    path = os.path.join(src_dir, config["buildfile_dir"])
    build_command = f"docker build --no-cache -t {image_name} ."
    build_process = subprocess.run(build_command.split(" "), cwd=path, capture_output=True)
    build_output = f"stdout:\n{build_process.stdout.decode('utf-8')}\nstderr:\n{build_process.stderr.decode('utf-8')}"
    logging.info(f"Output of '{build_command}':\n\n{build_output}")
    return_code = build_process.returncode
    logging.info(f"Command '{build_command}' exited with code {return_code}")
    return return_code, build_output

def check_env(config, src_dir, artifact_name, pkglist_path):
    """
    Builds a list of all software packages installed in the
    Docker image given in 'config', depending on the package managers
    specified in the configuration, then stores it in a CSV file.

    Parameters
    ----------
    config: dict
        Parsed config file.

    src_dir: str
        Path to the directory where the artifact is stored.

    artifact_name: str
        Name of the artifact. Used both as the Docker image name, and for the
        packages list for tracking purpose during the output analysis.

    pkglist_path: str
        Path to the package list file.

    Returns
    -------
    None
    """
    # Saving the current time to add it to every row:
    now = datetime.datetime.now()
    timestamp = str(datetime.datetime.timestamp(now))

    # Commands to list installed packages along with their versions and the name
    # of the package manager, depending on the package managers.
    # Each package manager is associated with a tuple, the first item being
    # the package manager's command, the second being the arguments for the
    # query (they must be separated for the "--entrypoint" argument of Docker
    # 'run', see below), and the third one being the command that will format
    # the output of the query command (this one can be an empty string in case
    # the formatting part is already done using the options of the first command).
    # The first command needs to be run on the container, and the second on the
    # host, to take into account container images that do not have the formatting
    # packages installed.
    pkgmgr_cmd = {
        "dpkg": ("dpkg",\
                 "-l",\
                 f"awk 'NR>5 {{print $2 \",\" $3 \",dpkg,{artifact_name},{timestamp}\"}}'"), \
        "rpm":("rpm",\
               f"-qa --queryformat '%{{NAME}},%{{VERSION}},rpm,{artifact_name},{timestamp}\\n'",\
               ""), \
        "pacman":("pacman",\
                  "-Q",\
                  f"awk '{{print $0 \",\" $1 \",pacman,{artifact_name},{timestamp}\"}}'"), \
        "pip":("pip",\
               "list",\
               f"awk 'NR>2 {{print $1 \",\" $2 \",\" \"pip,{artifact_name},{timestamp}\"}}'"), \
        "conda":("/root/.conda/bin/conda",\
                 "list -e",\
                 f"sed 's/=/ /g' | awk 'NR>3 {{print $1 \",\" $2 \",conda,{artifact_name},{timestamp}\"}}'")
    }
    # Command to obtain the latest commit hash in a git repository (separated
    # into 2 parts for "--entrypoint"):
    gitcmd = ("git", "log -n 1 --pretty=format:%H")

    logging.info("Checking software environment")
    pkglist_file = open(pkglist_path, "w")
    path = os.path.join(src_dir, config["buildfile_dir"])
    # Package managers:
    for pkgmgr in config["package_managers"]:
        # "--entrypoint" requires command and arguments to be separated.
        # This Docker 'run' option is used to prevent the shell from printing
        # a login message, if any.
        pkglist_cmd = pkgmgr_cmd[pkgmgr][0]
        pkglist_cmdargs = pkgmgr_cmd[pkgmgr][1].split(" ")
        listformat_cmd = pkgmgr_cmd[pkgmgr][2]
        logging.info(f"Checking '{pkgmgr}'")
        pkglist_process = subprocess.run(["docker", "run", "--rm", "--entrypoint", pkglist_cmd, artifact_name] + pkglist_cmdargs, cwd=path, capture_output=True)
        format_process = subprocess.run(f"cat << EOF | {listformat_cmd}\n{pkglist_process.stdout.decode('utf-8')}EOF", cwd=path, capture_output=True, shell=True)
        pkglist = format_process.stdout.decode("utf-8")
        pkglist_file.write(pkglist)

    # Python venvs:
    logging.info("Checking Python venvs")
    for venv in config["python_venvs"]:
        pipcmd = pkgmgr_cmd["pip"][0]
        pipcmd_args = pkgmgr_cmd["pip"][1]
        pkglist_process = subprocess.run(["docker", "run", "--rm", "-w", venv["path"], "--entrypoint", venv["path"] + "/bin/" + pipcmd, artifact_name] + pipcmd_args.split(" "), cwd=path, capture_output=True)
        format_process = subprocess.run(f"cat << EOF | {listformat_cmd}\n{pkglist_process.stdout.decode('utf-8')}EOF", cwd=path, capture_output=True, shell=True)
        pkglist = format_process.stdout.decode("utf-8")
        pkglist_file.write(pkglist)

    # Git packages:
    logging.info("Checking Git packages")
    for repo in config["git_packages"]:
        pkglist_process = subprocess.run(["docker", "run", "--rm", "-w", repo["location"], "--entrypoint", gitcmd[0], artifact_name] + gitcmd[1].split(" "), cwd=path, capture_output=True)
        repo_row = f"{repo['name']},{pkglist_process.stdout.decode('utf-8')},git,{artifact_name},{timestamp}"
        pkglist_file.write(f"{repo_row}\n")

    # Misc packages:
    logging.info("Checking miscellaneous packages")
    for pkg in config["misc_packages"]:
        logging.info(f"Downloading package {pkg['name']} from {pkg['url']}")
        with tempfile.NamedTemporaryFile() as pkg_file:
            pkg_hash = download_file_and_get_hash(pkg["url"], pkg_file.name)
        pkglist_file.write(f"{pkg['name']},{pkg_hash},misc,{artifact_name},{timestamp}\n")
    pkglist_file.close()

def remove_image(image_name):
    logging.info(f"Removing image '{image_name}'")
    subprocess.run(["docker", "rmi", image_name], capture_output = True)

def main():
    parser = argparse.ArgumentParser(
        prog = "ecg",
        description =
        """
        ECG is a program that automates software environment checking for scientific artifacts.
        It is meant to be executed periodically to analyze variations in the software environment of the artifact through time.
        """
    )
    parser.add_argument(
        "config",
        help = "The path to the configuration file of the artifact's Docker image."
    )
    parser.add_argument(
        "-p", "--pkg-list",
        help = "Path to the file where the package list generated by the program should be written.",
        required = True
    )
    parser.add_argument(
        "-b", "--build-status",
        help = "Path to the file where to write the build status of the Docker image given in the configuration file.",
        required = True
    )
    parser.add_argument(
        "-a", "--artifact-hash",
        help = "Path to the file where to write the log of the hash of the downloaded artifact.",
        required = True
    )
    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    config_path = args.config
    with open(config_path, "r") as config_file:
        config = json.loads(config_file.read())

    artifact_name = os.path.splitext(os.path.basename(config_path))[0]

    ecg(artifact_name, config, args.pkg_list, args.build_status, args.artifact_hash)

    return 0

def ecg(artifact_name, config, pkglist_path, buildstatus_path, arthashlog_path):
    # just in case Snakemake does not create them
    pathlib.Path(pkglist_path).touch()
    pathlib.Path(buildstatus_path).touch()
    pathlib.Path(arthashlog_path).touch()

    status = ""

    with tempfile.TemporaryDirectory() as tmp_dir:
        dl_dir = tmp_dir.name
        artifact_dir = download_sources(config["url"], config["type"], arthashlog_path, dl_dir, artifact_name)

        if artifact_dir != "":
            path = os.path.join(artifact_dir, config["buildfile_dir"])
            return_code, build_output = build_image(path, artifact_name)
            if return_code == 0:
                status = "success"
                check_env(config, artifact_dir, artifact_name, pkglist_path)
                remove_image(artifact_name)
            else:
                status = builderror_identifier(build_output)
        else:
            logging.fatal("Artifact could not be downloaded!")
            status = "artifact_unavailable"
        buildresult_saver(status, buildstatus_path, config_path)

if __name__ == "__main__":
    main()
