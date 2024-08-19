#!/bin/bash

OUTPUT_PATH=output
CACHE_DIR=cache
TESTFILE=$1

if [ ! -d $OUTPUT_PATH ]
then
    mkdir $OUTPUT_PATH
fi
if [ ! -d $CACHE_DIR ]
then
    mkdir $CACHE_DIR
fi

./ecg.py $TESTFILE -p $OUTPUT_PATH/pkglist.csv -b $OUTPUT_PATH/build_status.csv -a $OUTPUT_PATH/artifact_hash.csv -c $CACHE_DIR --docker-cache