#!/bin/bash

INPUT_DIR=$1

INPUT=$(find $INPUT_DIR/*.csv -maxdepth 1 -type f)
OUTPUT=$2

cat $INPUT > $OUTPUT