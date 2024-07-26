# Study of the Reproducibility and Longevity of Dockerfiles

ECG is a program that automates software environment checking for scientific artifacts.

It is meant to be executed periodically to analyze variations in the software environment of the artifact through time.

## How it works

ECG takes as input a JSON configuration telling where to download the artifact, where to find the Dockerfile to build in the artifact, and which package managers are used by the Docker container.

It will then download the artifact, build the Dockerfile, and then create a list of the installed packages in the Docker container. It also stores the potential errors encountered when building the Dockerfile, and logs the hash of the artifact for future comparison.

## Setup

A Linux operating system and the following packages are required:
- `python`
- `docker`
- `snakemake`
- `gawk`
- `nickel`
- `sed`

The following Python package is also required:
- `requests`

Otherwise, you can use the Nix package manager and run `nix develop` in this directory to setup the full software environment.

## Usage

Run `ecg.py` as follow:

```
python3 ecg.py <config_file> -p <pkglist_path> -l <log_file> -b <build_status_file> -a <artifact_hash_log> -c <cache_directory>
```

Where:
- `<config_file>` is the configuration file of the artifact in JSON format. An example is given in `artifacts_json/test.json`. WARNING: The name of the file (without the extension) must comply with the Docker image naming convention: only characters allowed are lowercase letters and numbers, separated with either one "." maximum, or two "_" maximum, or an unlimited number of "-", and should be of 128 characters maximum.
- `<pkglist_path>` is the path to the file where the package list generated by the program should be written.
- `<log_file>` is the path to the file where to log the output of the program.
- `<build_status_file>` is the path to the file where to write the build status of the Docker image given in the configuration file.
- `<artifact_hash_log>` is the path to the file where to log the hash of the downloaded artifact.
- `<cache_directory>` is the path to the cache directory, where downloaded artifacts will be stored for future usage. If not specified, cache is disabled.

## Output

### Package list

The list of packages installed in the container, depending on the package managers, Git packages and other miscellaneous packages given in the config file, in the form of a CSV file, with the following columns in order:

| Package name | Version | Package manager |
|--------------|---------|-----------------|

For Git packages, the hash of the last commit is used as version number. For miscellaneous packages, the hash of the file that has been used to install the package is used as version number.

### Output log

Just a plain text file containing the output of the script.

### Build status file

The log of the attempts to build the Docker image, in the form of a CSV file, with the following columns in order:

| Config file path | Timestamp | Result          |
|------------------|-----------|-----------------|

The timestamp corresponds to when the result is being logged, not to when it happened.

The following are the possible results of the build:
- `success`: The Docker image has been built successfully.
- `package_unavailable`: A command requested the installation of a package that is not available.
- `baseimage_unavailable`: The base image needed for this container is not available.
- `artifact_unavailable`: The artifact could not be downloaded.
- `dockerfile_not_found`: No Dockerfile has been found in the location specified in the configuration file.
- `unknown_error`: Any other error.

### Artifact hash log

The log of the hash of the artifact archive file, in the form of a CSV file, with the following columns in order:

| Timestamp | Hash |
|-----------|------|

The timestamp corresponds to when the hash has been logged, not to when the artifact has been downloaded.

## License

This project is licensed under the GNU General Public License version 3. You can find the terms of the license in the file LICENSE.