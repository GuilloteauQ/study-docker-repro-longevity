#!/bin/python3

"""
    This script performs a software environment analysis on the outputs
    of the workflow to generate tables that can then be plotted by another
    program.
"""

import argparse
import csv
import os
import datetime

# All possible package sources, initialized to 0.
# This is required to make the column of the result table deterministic,
# so they can be determined without the header in the CSV file.
pkgsources = {"dpkg":0, "rpm":0, "pacman":0, "pip":0, "conda":0, "git":0, "misc":0}

def sources_stats(input_table, pkgsources):
    """
    Analyzes the given package lists table to determine the number of artifacts
    using a package manager, Git packages or misc packages.

    Parameters
    ----------
    input_table: str
        Table to analyse.

    pkgsources: dict
        A dictionnary that contains all the possible package sources as keys,
        with all keys' value initialized at 0.

    Returns
    -------
    dict
        Output table of the analysis in the form of a dict with headers as keys.
    """
    i = 0
    for row in input_table:
        # Third column is the package source:
        if row[2] not in pkgsources:
            pkgsources[row[2]] = 1
        else:
            pkgsources[row[2]] += 1
    return pkgsources

def pkg_changed(table, artifact_name, pkgname, pkgsource):
    """
    Analyzes the given package lists table to determine if the given package
    changed for the given artifact.

    Parameters
    ----------
    table: str
        Table to analyse.

    artifact_name: str
        Name of the artifact for which we want to analyze package changes.

    pkgname: str
        The package we want to track changes.

    pkgsource: str
        Source of the package, in case there is multiple packages with the
        same name but different sources.

    Returns
    -------
    changed: bool
        True if the version number of the package changed over time, False
        otherwise.
    """
    changed = False
    i = 0
    pkgver = ""
    while i < len(table) and not changed:
        row = table[i]
        # Artifact name is in the 4th column, package name in the first,
        # and package source in the 3rd:
        if row[3] == artifact_name and row[0] == pkgname and row[2] == pkgsource:
            # If the first version number has not been saved yet:
            if pkgver == "":
                pkgver = row[1] # Package version is in the 2nd column
            elif row[1] != pkgver:
                changed = True
        i += 1
    return changed

def pkgs_changes(input_table, pkgsources):
    """
    Analyzes the given package lists table to determine the number of packages
    that changed for every package source.

    Parameters
    ----------
    input_table: str
        Table to analyse.

    pkgsources: dict
        A dictionnary that contains all the possible package sources as keys,
        with all keys' value initialized at 0.

    Returns
    -------
    dict
        Output table of the analysis in the form of a dict with headers as keys.
    """
    # Key is the artifact name, and value is a list of tuples constituted
    # of the package that has been checked and its source for this artifact:
    # FIXME: Memory usage?
    checked_artifacts = {}
    i = 0
    for row in input_table:
        artifact_name = row[3] # Artifact name is in the 4th column
        if artifact_name not in checked_artifacts.keys():
            checked_artifacts[artifact_name] = []
        pkgname = row[0] # Package name is in the first column
        pkgsource = row[2] # Package source is in the 3rd column
        if (pkgname, pkgsource) not in checked_artifacts[artifact_name]:
            if pkg_changed(input_table, artifact_name, pkgname, pkgsource):
                pkgsources[pkgsource] += 1
            checked_artifacts[artifact_name].append((pkgname, pkgsource))
    return pkgsources

def pkgs_per_container(input_table):
    print("ERROR: Not implemented!")

def main():
    # Command line arguments parsing:
    parser = argparse.ArgumentParser(
        prog = "softenv_analysis",
        description =
        """
        This script performs a software environment analysis on the outputs
        of the workflow to generate tables that can then be plotted
        by another program.
        """
    )
    parser.add_argument(
        "-v", "--verbose",
        action = "store_true",
        help = "Shows more details on what is being done."
    )
    parser.add_argument(
        "-t", "--analysis-type",
        help =
        """
        Specify the type of software analysis to run. Depending on the
        type of analysis, multiple tables can be generated:
        the number of packages per source (a package manager, git or misc)
        by using `sources-stats`,
        the number of packages that changed over time (0 if only
        one file is given, since it will only include the package list
        of a single execution) by using `pkg-changes`,
        the number of packages per container by specifying `pkgs-per-container`.
        """,
        choices = ["sources-stats", "pkgs-changes", "pkgs-per-container"],
        required = True
    )
    parser.add_argument(
        "-i", "--input",
        action = "append",
        nargs = "+",
        help =
        """
        The CSV file used as input for the analysis function. Multiple files
        can be specified at once by separating them with a space.
        All the input files must be package lists generated by ECG.
        """,
        required = True
    )
    parser.add_argument(
        "-o", "--output",
        help =
        """
        Path to the output CSV file that will be created by the analysis function.
        """,
        required = True
    )
    args = parser.parse_args()
    inputs = args.input
    output_path = args.output
    analysis_type = args.analysis_type

    # Parsing the input files:
    input_table = []
    for i in inputs:
        for path in i:
            input_file = open(path)
            input_table += list(csv.reader(input_file))
            input_file.close()

    # Analyzing the inputs:
    if analysis_type == "sources-stats":
        output_dict = sources_stats(input_table, pkgsources)
    elif analysis_type == "pkgs-changes":
        output_dict = pkgs_changes(input_table, pkgsources)
    elif analysis_type == "pkgs-per-container":
        output_dict = pkgs_per_container(input_table)
    # Adding the current time to every row:
    now = datetime.datetime.now()
    timestamp = str(datetime.datetime.timestamp(now))
    output_dict["timestamp"] = timestamp

    # Writing analysis to output file:
    output_file = open(output_path, "w+")
    dict_writer = csv.DictWriter(output_file, fieldnames=output_dict.keys())
    # dict_writer.writeheader()
    dict_writer.writerow(output_dict)
    output_file.close()

if __name__ == "__main__":
    main()