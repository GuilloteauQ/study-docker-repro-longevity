#!/bin/bash

DATE=$(date +%Y%m%d)

rm -f blacklists/$DATE.csv
rm -rf outputs
snakemake --cores 4