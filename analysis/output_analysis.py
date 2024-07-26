#!/bin/python3

"""
    This script will analyze the outputs from ECG to generate tables that will
    be later plotted.
"""

import argparse
import csv
import os

def softenv_analysis(input_table):
    """
    Analyzes the given package lists table to determine the number of artifacts
    using a package manager, Git packages or misc packages.

    Parameters
    ----------
    input_table: str
        Table to analyse.

    Returns
    -------
    dict
        Output table of the analysis in the form of a dict with headers as keys.
    """
    pkgmgr = {}
    for row in input_table:
        # Third column is the package source:
        if row[2] in pkgmgr:
            pkgmgr[row[2]] += 1
        else:
            pkgmgr[row[2]] = 1
    return pkgmgr

def artifact_analysis(input_table):
    """
    Analyzes the given artifact hash table to determine the number of artifacts
    that change through time.

    Parameters
    ----------
    input_table: str
        Table to analyse.

    Returns
    -------
    dict
        Output table of the analysis in the form of a dict with headers as keys.
    """
    return {}

def buildstatus_analysis(input_table):
    """
    Analyzes the given build status table.

    Parameters
    ----------
    input_table: str
        Table to analyse.

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
    input_table = []
    for input_path in os.listdir(input_dir):
        input_file = open(os.path.join(input_dir, input_path))
        input_table += list(csv.reader(input_file))
        input_file.close()

    # Analyzing the inputs:
    output_file = open(output_path, "w+")
    output_dict = {}
    if analysis_type == "soft-env":
        output_dict = softenv_analysis(input_table)
    elif analysis_type == "artifact":
        output_dict = artifact_analysis(input_table)
    elif analysis_type == "build-status":
        output_dict = buildstatus_analysis(input_table)
    # Writing analysis to output file:
    dict_writer = csv.DictWriter(output_file, fieldnames=output_dict.keys())
    dict_writer.writeheader()
    dict_writer.writerow(output_dict)
    output_file.close()

if __name__ == "__main__":
    main()