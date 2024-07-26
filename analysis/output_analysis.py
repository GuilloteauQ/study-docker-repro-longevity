#!/bin/python3

"""
    This script will analyze the outputs from ECG to generate tables that will
    be later plotted.
"""

import argparse
import csv
import os

def softenv_analysis(input_tables):
    """
    Analyzes the given package lists tables to determine the number of artifacts
    using a package manager, Git packages or misc packages.

    Parameters
    ----------
    input_tables: str
        Tables to analyse.

    Returns
    -------
    dict
        Output table of the analysis in the form of a dict with headers as keys.
    """
    pkgmgr = {}
    for table in input_tables:
        for row in table:
            # Third column is the package source:
            if row[2] not in pkgmgr:
                pkgmgr[row[2]] = 1
            else:
                pkgmgr[row[2]] += 1
    return pkgmgr

def artifact_changed(table):
    """
    Indicates whether the artifact involved in the given hash log table
    has changed over time.

    Parameters
    ----------
    table: list
        Artifact hash log table.

    Returns
    -------
    bool
        True if artifact changed, False otherwise.
    """
    changed = False
    # Hash is in the 2nd column:
    artifact_hash = table[0][1]
    i = 0
    while i < len(table) and not changed:
        if table[i][1] != artifact_hash:
            changed = True
        i += 1
    return changed

def artifact_available(table):
    """
    Indicates whether the artifact involved in the given hash log table
    is still available.

    Parameters
    ----------
    table: list
        Artifact hash log table.

    Returns
    -------
    bool
        True if artifact is still available, False otherwise.
    """
    available = True
    # We check the last line to check current availability:
    if table[-1][1] == "":
        available = False
    return available

def artifact_analysis(input_tables):
    """
    Analyzes the given artifact hash tables to determine if the artifacts are
    still available and didn't change, changed, or aren't available anymore.

    Parameters
    ----------
    input_tables: str
        Table to analyse.

    Returns
    -------
    dict
        Output table of the analysis in the form of a dict with headers as keys.
    """
    artifacts = {"available":0, "unavailable":0, "changed":0}
    for table in input_tables:
        if artifact_available(table):
            artifacts["available"] += 1
        else:
            artifacts["unavailable"] += 1
        if artifact_changed(table):
            artifacts["changed"] += 1
    return artifacts

def buildstatus_analysis(input_tables):
    """
    Analyzes the given build status tables.

    Parameters
    ----------
    input_tables: str
        Tables to analyse.

    Returns
    -------
    dict
        Output table of the analysis in the form of a dict with headers as keys.
    """
    return {}

def main():
    # Command line arguments parsing:
    parser = argparse.ArgumentParser(
        prog = "output_analysis",
        description = "This script analyzes the outputs from ECG to create " \
            "tables."
    )
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        help = "Shows more details on what is being done."
    )
    parser.add_argument(
        "-t", "--analysis-type",
        help = "Specify the type of analysis to run.",
        choices = ["soft-env", "artifact", "build-status"],
        required = True
    )
    parser.add_argument(
        "input_dir",
        help = "Path to the directory where the CSV files used as input for " \
            "the analysis function are stored. They must be all outputs from ECG."
    )
    parser.add_argument(
        "output_path",
        help = "Path to the output CSV file that will be created by the " \
            "analysis function."
    )
    args = parser.parse_args()

    analysis_type = args.analysis_type
    input_dir = args.input_dir
    output_path = args.output_path

    # Parsing the inputs from the directory:
    input_tables = []
    for input_path in os.listdir(input_dir):
        input_file = open(os.path.join(input_dir, input_path))
        input_tables.append(list(csv.reader(input_file)))
        input_file.close()

    # Analyzing the inputs:
    output_file = open(output_path, "w+")
    output_dict = {}
    if analysis_type == "soft-env":
        output_dict = softenv_analysis(input_tables)
    elif analysis_type == "artifact":
        output_dict = artifact_analysis(input_tables)
    elif analysis_type == "build-status":
        output_dict = buildstatus_analysis(input_tables)
    # Writing analysis to output file:
    dict_writer = csv.DictWriter(output_file, fieldnames=output_dict.keys())
    dict_writer.writeheader()
    dict_writer.writerow(output_dict)
    output_file.close()

if __name__ == "__main__":
    main()