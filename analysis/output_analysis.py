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
    i = 0
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
    Analyzes the given build status tables to count the results of the building
    of the Dockerfile for each category.

    Parameters
    ----------
    input_tables: str
        Tables to analyse.

    Returns
    -------
    dict
        Output table of the analysis in the form of a dict with headers as keys.
    """
    buildstatus = {}
    for table in input_tables:
        # # There has never been any error:
        # if table == [[]]:
        #     if "never_failed" not in buildstatus:
        #             buildstatus["never_failed"] = 1
        #     else:
        #         buildstatus["never_failed"] += 1
        # # There has been an error at least once:
        # else:
        for row in table:
            # Third column is the result:
            if row[2] not in buildstatus:
                buildstatus[row[2]] = 1
            else:
                buildstatus[row[2]] += 1
    return buildstatus

def main():
    # Command line arguments parsing:
    parser = argparse.ArgumentParser(
        prog = "output_analysis",
        description = "This script analyzes the outputs from ECG to create " \
            "tables."
    )
    parser.add_argument(
        "-v", "--verbose",
        action = "store_true",
        help = "Shows more details on what is being done."
    )
    parser.add_argument(
        "-t", "--analysis-type",
        help = "Specify the type of analysis to run.",
        choices = ["soft-env", "artifact", "build-status"],
        required = True
    )
    parser.add_argument(
        "-i", "--input",
        action = "append",
        help = "The CSV file used as input for the analysis function." \
            "Multiple files can be specified by repeating this argument" \
            "with different paths. All the input files must be outputs" \
            "from ECG.",
        required = True
    )
    parser.add_argument(
        "-o", "--output",
        help = "Path to the output CSV file that will be created by the " \
            "analysis function.",
        required = True
    )
    args = parser.parse_args()

    analysis_type = args.analysis_type
    input_paths = args.input
    output_path = args.output

    # Parsing the input files:
    input_tables = []
    for path in input_paths:
        input_file = open(path)
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