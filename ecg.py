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

def trim(url) :
    """
    Trims given url for cache storage.

    Parameters
    ----------
    url: str
        URL to trim.

    Returns
    -------
    str
        Trimmed URL.
    """
    trimmed = ""
    for c in url.lower():
        if c not in "/:;\\'\" *?":
            trimmed += c

    return trimmed

def download_file(url, dest):
    """
    Downloads the file stored at the given URL and returns its hash
    and location.

    Parameters
    ----------
    url: str
        URL to the file to download.
    dest: str
        Path to where the file should be stored.

    Returns
    -------
    str
       Hash of the downloaded file.
    """
    req = requests.get(url)
    file = open(dest, "wb")
    file.write(req.content)
    file.close()
    hash_process = subprocess.run(f"sha256sum {file.name} | cut -d ' ' -f 1 | tr -d '\n'", capture_output=True, shell=True)
    return hash_process.stdout.decode("utf-8")

def download_sources(config, arthashlog_path, dl_dir, use_cache):
    """
    Downloads the source of the artifact in 'config'.

    Parameters
    ----------
    config: dict
        Parsed config file.

    arthashlog_path: str
        Path to the artifact hash log file.

    dl_dir: str
        Path to the directory where to download the artifact.

    use_cache: bool
        Indicates whether the cache should be used or not.

    Returns
    -------
    temp_dir: str
        Path to the directory where the artifact is downloaded to.
    """
    url = config["artifact_url"]
    artifact_name = trim(url)
    artifact_dir = os.path.join(dl_dir, artifact_name)
    # Checking if artifact in cache. Not downloading if it is:
    if not os.path.exists(artifact_dir) or not use_cache:
        logging.info(f"Downloading artifact from {url}")
        # In case cache was used before:
        if not use_cache:
            os.system(f"rm -rf {artifact_dir}")
        os.mkdir(artifact_dir)
        artifact_file = tempfile.NamedTemporaryFile()
        artifact_path = artifact_file.name
        artifact_hash = download_file(url, artifact_path)
        if config["type"] == "zip":
            artifact = zipfile.ZipFile(artifact_path)
        elif config["type"] == "tar":
            artifact = tarfile.open(artifact_path)
        logging.info(f"Extracting artifact at {artifact_dir}")
        artifact.extractall(artifact_dir)
        # Logging the current hash of the artifact:
        arthashlog_file = open(arthashlog_path, "a")
        now = datetime.datetime.now()
        timestamp = str(datetime.datetime.timestamp(now))
        arthashlog_file.write(f"{timestamp},{artifact_hash}\n")
        arthashlog_file.close()
    else:
        logging.info(f"Cache found for {url}, skipping download")
    return artifact_dir

def buildstatus_saver(output, buildstatus_path, config_path):
    """
    Parses the given 'output' to indentify the errors, then saves them to the
    'build_status' file.

    Parameters
    ----------
    output: str
        Output of Docker.

    buildstatus_path: str
        Path to the build status file.

    config_path: str
        Path to the config file.

    Returns
    -------
    None
    """
    # Possible error messages given by 'docker build' and their category.
    # The key is the category, the value is a tuple of error messages belonging to
    # to this category:
    build_errors = {
        "package_unavailable":("Unable to locate package"),
        "baseimage_unavailable":("manifest unknown: manifest unknown")
    }

    file_exists = os.path.exists(buildstatus_path)
    buildstatus_file = open(buildstatus_path, "a")
    artifact_name = os.path.basename(config_path).split(".")[0]
    # # Writing header in case file didn't exist:
    # if not file_exists:
    #     buildstatus_file.write("yaml_path,timestamp,error")
    unknown_error = True
    for error_cat, error in build_errors.items():
        if error in output:
            unknown_error = False
            now = datetime.datetime.now()
            timestamp = str(datetime.datetime.timestamp(now))
            buildstatus_file.write(f"{artifact_name},{timestamp},{error_cat}\n")
    if unknown_error:
        now = datetime.datetime.now()
        timestamp = str(datetime.datetime.timestamp(now))
        buildstatus_file.write(f"{artifact_name},{timestamp},unknown_error\n")
    buildstatus_file.close()

def build_image(config, src_dir):
    """
    Builds the given Docker image in 'config'.

    Parameters
    ----------
    config: dict
        Parsed config file.

    src_dir: str
        Path to the directory where the artifact is stored.

    Returns
    -------
    return_code: bool, build_output: str
        Return code and output of Docker 'build'.
    """
    name = config["image_name"]
    logging.info(f"Starting building image {name}")
    path = os.path.join(src_dir, config["dockerfile_location"])
    build_command = f"docker build -t {config['image_name']} ."
    build_process = subprocess.run(build_command.split(" "), cwd=path, capture_output=True)
    build_output = f"stdout:\n{build_process.stdout.decode('utf-8')}\nstderr:\n{build_process.stderr.decode('utf-8')}"
    # build_output = build_process.stderr.decode("utf-8")
    logging.info(f"Output of '{build_command}':")
    logging.info(build_output)
    return_code = build_process.returncode
    logging.info(f"Command '{build_command}' exited with code {return_code}")
    return return_code, build_output

def check_env(config, src_dir, pkglist_path):
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

    pkglist_path: str
        Path to the package list file.

    Returns
    -------
    None
    """
    # Commands to list installed packages along with their versions and the name
    # of the package manager, depending on the package managers.
    # Each package manager is associated with a tuple, the first item being
    # the package manager's command, the second being the arguments for the
    # query (they must be separate for the "--entrypoint" argument of Docker
    # 'run', see below), and the third one being the command that will format
    # the output of the query command (this one can be an empty string in case
    # the formatting part is already done using the options of the first command).
    # The first command needs to be run on the container, and the second on the
    # host, to take into account container images that do not have the formatting
    # packages installed.
    pkgmgr_cmd = {
        "dpkg": ("dpkg", "-l", "awk 'NR>5 {print $2 \",\" $3 \",\" \"dpkg\"}'"), \
        "rpm":("rpm", "-qa --queryformat '%{NAME},%{VERSION},rpm\\n'", ""), \
        "pacman":("pacman", "-Q", "awk '{print $0 \",\" $1 \",pacman\"}'"), \
        "pip":("pip", "freeze", "sed 's/==/,/g' | awk '{print $0 \",pip\"}'"), \
        "conda":("/root/.conda/bin/conda", "list -e", "sed 's/=/ /g' | awk 'NR>3 {print $1 \",\" $2 \",conda\"}'")
    }
    # Command to obtain the latest commit hash in a git repository (separated
    # into 2 parts for "--entrypoint"):
    gitcmd = ("git", "log -n 1 --pretty=format:%H")

    logging.info("Checking software environment")
    pkglist_file = open(pkglist_path, "w")
    # pkglist_file.write("package,version,package_manager\n")
    path = os.path.join(src_dir, config["dockerfile_location"])
    for pkgmgr in config["package_managers"]:
        # "--entrypoint" requires command and arguments to be separated.
        # This Docker 'run' option is used to prevent the shell from printing
        # a login message, if any.
        pkglist_cmd = pkgmgr_cmd[pkgmgr][0]
        pkglist_cmdargs = pkgmgr_cmd[pkgmgr][1].split(" ")
        listformat_cmd = pkgmgr_cmd[pkgmgr][2]
        logging.info(f"Checking '{pkgmgr}'")
        # pkglist_process = subprocess.run(["docker", "run", "--rm", config["image_name"]] + pkglist_cmd.split(" "), cwd=path, capture_output=True)
        pkglist_process = subprocess.run(["docker", "run", "--rm", "--entrypoint", pkglist_cmd, config["image_name"]] + pkglist_cmdargs, cwd=path, capture_output=True)
        format_process = subprocess.run(f"cat << EOF | {listformat_cmd}\n{pkglist_process.stdout.decode('utf-8')}EOF", cwd=path, capture_output=True, shell=True)
        pkglist = format_process.stdout.decode("utf-8")
        pkglist_file.write(pkglist)
    if "git_packages" in config.keys():
        logging.info("Checking Git packages")
        for repo in config["git_packages"]:
            pkglist_process = subprocess.run(["docker", "run", "--rm", "-w", repo["location"], "--entrypoint", gitcmd[0], config["image_name"]] + gitcmd[1].split(" "), cwd=path, capture_output=True)
            repo_row = f"{repo['name']},{pkglist_process.stdout.decode('utf-8')},git"
            pkglist_file.write(f"{repo_row}\n")
    if "misc_packages" in config.keys():
        logging.info("Checking packages obtained outside of a package manager or VCS")
        for pkg in config["misc_packages"]:
            logging.info(f"Downloading package {pkg['name']} from {pkg['url']}")
            pkg_file = tempfile.NamedTemporaryFile()
            pkg_path = pkg_file.name
            pkg_hash = download_file(pkg["url"], pkg_path)
            pkg_row = f"{pkg['name']},{pkg_hash},misc"
            pkglist_file.write(f"{pkg_row}\n")
    pkglist_file.close()

def remove_image(config):
    """
    Removes the Docker image given in 'config'.

    Parameters
    ----------
    config: dict
        Parsed config file.

    Returns
    -------
    None
    """
    name = config["image_name"]
    logging.info(f"Removing image '{name}'")
    subprocess.run(["docker", "rmi", name], capture_output = True)

def main():
    # Paths:
    config_path = ""
    pkglist_path = "" # Package list being generated
    buildstatus_path = "" # Summary of the build process of the image
    arthashlog_path = "" # Log of the hash of the downloaded artifact
    cache_dir = "" # Artifact cache directory, when using one. 'None' value indicates no cache.
    use_cache = False

    # Command line arguments parsing:
    parser = argparse.ArgumentParser(
        prog = "ecg",
        description = "ECG is a program that automates software environment checking for scientific artifacts. "
            "It is meant to be executed periodically to analyze variations in the software environment of the artifact through time."
    )
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = "Shows more details on what is being done."
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
        "-l", "--log-path",
        help = "Path to the file where to log the output of the program.",
        required = True
    )
    parser.add_argument(
        "-b", "--build-summary",
        help = "Path to the file where to write the build summary of the Docker image given in the configuration file.",
        required = True
    )
    parser.add_argument(
        "-a", "--artifact-hash",
        help = "Path to the file where to write the log of the hash of the downloaded artifact.",
        required = True
    )
    parser.add_argument(
        "-c", "--cache-dir",
        help = "Path to the cache directory, where artifacts that are downloaded will be stored for future usage. " \
                "If not specified, cache is disabled.",
        required = False
    )
    args = parser.parse_args()

    # Setting up the paths of the outputs:
    log_path = "log.txt" # Output of the program
    pkglist_path = args.pkg_list
    log_path = args.log_path
    buildstatus_path = args.build_summary
    arthashlog_path = args.artifact_hash
    cache_dir = args.cache_dir

    # Setting up the log: will be displayed both on stdout and to the specified
    # file:
    print(f"Output will be stored in {log_path}")
    logging.basicConfig(filename = log_path, filemode = "w", format = '%(levelname)s: %(message)s', level = logging.INFO)
    verbose = args.verbose
    if verbose:
       logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # Parsing the input file including the configuration of the artifact's
    # image:
    config_path = args.config
    config_file = open(config_path, "r")
    config = json.loads(config_file.read())
    # config = yaml.safe_load(config_file)
    # print(config)
    config_file.close()

    dl_dir = None
    # If not using cache, creates a temporary directory:
    if cache_dir == None:
        tmp_dir = tempfile.TemporaryDirectory()
        dl_dir = tmp_dir.name
    else:
        use_cache = True
        dl_dir = cache_dir
    artifact_dir = download_sources(config, arthashlog_path, dl_dir, use_cache)
    return_code, build_output = build_image(config, artifact_dir)
    if return_code == 0:
        check_env(config, artifact_dir, pkglist_path)
        remove_image(config)
        # Creates file if not already:
        pathlib.Path(buildstatus_path).touch()
    else:
        # Creates file if not already:
        pathlib.Path(pkglist_path).touch()
        buildstatus_saver(build_output, buildstatus_path, config_path)

if __name__ == "__main__":
    main()
