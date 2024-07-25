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
    usinga package manager, Git packages or misc packages.

    Parameters
    ----------
    input_table: str
        Table to analyse.

    Returns
    -------
    list
        Output table of the analysis.
    """
    return []

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
    list
        Output table of the analysis.
    """
    return []

def buildstatus_analysis(input_table):
    """
    Analyzes the given build status table.

    Parameters
    ----------
    input_table: str
        Table to analyse.

    Returns
    -------
    list
        Output table of the analysis.
    """
    return []

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
    os.chdir(input_dir)
    for input_path in os.listdir():
        input_file = open(input_path)
        input_table += list(csv.reader(input_file))
        print(input_table)
        input_file.close()

    # Analyzing the inputs:
    output_file = open(output_path, "w+")
    if analysis_type == "soft-env":
        output_file.writelines(softenv_analysis(input_table))
    elif analysis_type == "artifact":
        output_file.writelines(artifact_analysis(input_table))
    elif analysis_type == "build-status":
        output_file.writelines(buildstatus_analysis(input_table))
    output_file.close()

if __name__ == "__main__":
    main()