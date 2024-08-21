# Study of the Reproducibility and Longevity of Dockerfiles

The aim of this study is to show the current practices with Docker in High Performance Computing (HPC) conferences' artifacts.

This repository contains the code and the artifacts used for the study.

## Components of the workflow

The workflow is managed by Snakemake. Below are brief explanations on the various components of this workflow. Further details can be found in the chapter "Usage".

### Artifact configuration files

This repository contains configuration files for multiple artifacts from HPC conferences. These configuration files contain multiple informations that are used by ECG to build the Docker container and perform a software environment analysis.

You can suggest your own configuration files by following the protocol given inside the `protocol` directory (protocol is still WIP).

### ECG

ECG is a program that automates software environment checking for scientific artifacts that use Docker. It takes as input a JSON configuration telling where to download the artifact, where to find the Dockerfile to build in the artifact, and which package sources are used by the Docker container.

It will then download the artifact, build the Dockerfile, and then create a list of the installed packages in the Docker container (if it was built successfully). It also stores the potential errors encountered when building the Dockerfile, and logs the hash of the artifact for future comparison.

It is meant to be executed periodically to analyze variations in the software environment of the artifact through time.

Supported package sources:
- `dpkg`
- `rpm`
- `pacman`
- `pip`
- `conda`
- `git`
- `misc` *(miscellaneous packages are packages that have been installed outside of a package manager or VCS such as Git)*

### Analysis

Multiple type of analysis are done with the output of ECG to create tables that can later be plotted. The analysis done for this study are software environment, artifact, and build status analysis. Each type of analysis is done through a different script.

### Plots with R

The plotting script can generate both line and bar plots using the analysis results.

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

### Running the whole workflow

First, open `config/config.yaml` and change `system` to `local` if you try to run the workflow outside of the Grid'5000 testbed.

Then, run the following command at the root directory of the repository:
```
snakemake --cores <nb_cores>
```

Where `<nb_cores>` is the number of cores you want to assign to the workflow. The number of cores determine the number of instances of ECG that can run in parallel, so you may want to assign as many cores as possible here.

### Running each component separately

#### Artifact configuration files

Under `artifacts/nickel`, you will find some configuration files in the Nickel format. You will need to run the following command to convert a configuration file in the JSON format to make it readable for ECG and to check for errors:

```
nickel export --format json --output <output_path> <<< 'let {Artifact, ..} = import "'workflow/nickel/artifact_contract.ncl'" in ((import "'<input_config>'") | Artifact)'
```

Where:
- `<input_config>` is the configuration file in the Nickel format to check and convert to JSON.
- `<output_path>` is the path where to store the converted configuration file.

#### ECG

Run `ecg.py` as follow:

```
python3 ecg.py <config_file> -p <pkglist_path> -b <build_status_file> -a <artifact_hash_log> -c <cache_directory>
```

Where:
- `<config_file>` is the configuration file of the artifact in JSON format. WARNING: The name of the file (without the extension) must comply with the Docker image naming convention: only characters allowed are lowercase letters and numbers, separated with either one "." maximum, or two "_" maximum, or an unlimited number of "-", and should be of 128 characters maximum.
- `<pkglist_path>` is the path to the file where the package list generated by the program should be written.
- `<build_status_file>` is the path to the file where to write the build status of the Docker image given in the configuration file.
- `<artifact_hash_log>` is the path to the file where to log the hash of the downloaded artifact.
- `<cache_directory>` is the path to the cache directory, where downloaded artifacts will be stored for future usage. If not specified, cache is disabled.

You can also use `--docker-cache` to enable the cache of the Docker layers.

##### Outputs

###### Package list

The list of packages installed in the container, depending on the sources (a package manager, `git` or `misc`) given in the config file, in the form of a CSV file, with the following columns in order:

| Package name | Version | Source          | Config name | Timestamp |
|--------------|---------|-----------------|-------------|-----------|

For Git packages, the hash of the last commit is used as version number. For miscellaneous packages, the hash of the file that has been used to install the package is used as version number. The timestamp corresponds to the time when ECG started building the package list, so it will be the same for each package that has been logged during the same execution of ECG.

###### Build status file

The log of the attempts to build the Docker image, in the form of a CSV file, with the following columns in order:

| Config name | Timestamp | Result          |
|-------------|-----------|-----------------|

The timestamp corresponds to when the result is being logged, not to when it happened.

The following are the possible results of the build:
- `success`: The Docker image has been built successfully.
- `package_install_failed`: A command requested the installation of a package that failed.
- `baseimage_unavailable`: The base image needed for this container is not available.
- `artifact_unavailable`: The artifact could not be downloaded.
- `dockerfile_not_found`: No Dockerfile has been found in the location specified in the configuration file.
- `script_crash`: An error has occurred with the script itself.
- `job_time_exceeded`: When running on a batch system such as OAR, this error indicates that the script exceeded the allocated run time and had to be terminated.
- `unknown_error`: Any other error.

###### Artifact hash log

The log of the hash of the artifact archive file, in the form of a CSV file, with the following columns in order:

| Timestamp | Hash | Config name |
|-----------|------|-------------|

The timestamp corresponds to when the hash has been logged, not to when the artifact has been downloaded. If the artifact couldn't be downloaded, the hash is equal to `-1`.

#### Analysis

Under the folder `analysis`, you will find multiple analysis scripts. These scripts take as input the outputs of ECG to generate tables that can then be plotted by another program.

All the analysis scripts can be run the same way:

```
python3 <analysis_script> -i <input_table1> -i <input_table2> ... -o <output_table>
```

Where:
- `<analysis_script>` is one of the following analysis scripts.
- `<input_table1>`, `<input_table2>`... are one or more output tables from ECG. The required ECG output depends on the analysis script, see below.
- `<output_table>` is the path where to store the table generated by the analysis script.

*TODO: explain the content of the output files*

##### Software environment analysis

The script `softenv_analysis.py` performs a software environment analysis by parsing one or more package lists generated by ECG.

Depending on the type of analysis, multiple tables can be generated:
- `sources-stats`: Number of packages per source (a package manager, `git` or `misc`).
- `pkgs-changes`: Number of packages that changed over time (`0` if only one file is given, since it will only include the package list of a single execution).

The type of analysis can be specified using the option `-t`.

##### Artifact analysis

The script `artifact_analysis.py` performs an artifact analysis by parsing one or more artifact hash logs generated by ECG.

The table generated by this script gives the amount of artifacts that are available or not available, and the amount of artifacts that have been modified over time.

##### Build status analysis

The script `buildstatus_analysis.py` performs a build status analysis by parsing one or more build status log generated by ECG.

The table generated by this script gives the amount of images that have been built successfully, and the amount of images that failed to build, for each category of error.

#### Plots with R

Under the directory `plot`, you will find a `plot.r` script. Run it as follow:

```
Rscript plot.r <plot_type> <analysis_table> <output_plot> <column1> <column2> ...
```

Where:
- `<plot_type>` is either `line` or `bar` depending if you want to produce a line or a bar plot from the given table.
- `<analysis_table>` is the path to the analysis table produced by an analysis script.
- `<output_plot>` is the path where the script will store the generated plot.
- `<column1> <column2> ...` are the headers of the columns of the given table.

## License

This project is licensed under the GNU General Public License version 3. You can find the terms of the license in the file LICENSE.