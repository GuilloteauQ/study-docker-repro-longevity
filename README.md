# Study of the Reproducibility and Longevity of Dockerfiles

ECG is a program that automates software environment checking for scientific artifacts.

It is meant to be executed periodically to analyze variations in the software environment of the artifact through time.

## How it works

ECG takes as input a JSON configuration telling where to download the artifact, where to find the Dockerfile to build in the artifact, and which package managers are used by the Docker container.

It will then download the artifact, build the Dockerfile, and then create a list of the installed packages in the Docker container. It also stores the potential errors encountered when building the Dockerfile, and logs the hash of the artifact for future comparison.

## Setup

A Linux operating system and the following packages are required:
- `snakemake`
- `gawk`
- `nickel`

The following Python package is also required:
- `requests`

Otherwise, you can use the Nix package manager and run `nix develop` in this directory to setup the full software environment.

## Usage

Run `ecg.py` as follow:

```
python3 ecg.py <config_file> -p <pkglist_path> -l <log_file> -b <build_status_file> -a <artifact_hash_log> -c <cache_directory>
```

Where:
- `<config_file>` is the configuration file of the artifact in JSON format. An example is given in `artifacts_json/test.json`.
- `<pkglist_path>` is the path to the file where the package list generated by the program should be written.
- `<log_file>` is the path to the file where to log the output of the program.
- `<build_status_file>` is the path to the file where to write the build summary of the Docker image given in the configuration file.
- `<artifact_hash_log>` is the path to the file where to log the hash of the downloaded artifact.
- `<cache_directory>` is the path to the cache directory, where downloaded artifacts will be stored for future usage.

## License

This project is licensed under the GNU General Public License version 3. You can find the terms of the license in the file LICENSE.