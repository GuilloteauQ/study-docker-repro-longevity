#!/bin/bash

OUTPUT_PATH=output
CACHE_DIR=cache
TESTFILE=test.yaml

if [ ! -d $OUTPUT_PATH ]
then
    mkdir $OUTPUT_PATH
fi
if [ ! -d $CACHE_DIR ]
then
    mkdir $CACHE_DIR
fi

./ecg.py $TESTFILE -p $OUTPUT_PATH/pkglist.csv -l $OUTPUT_PATH/log.txt -b $OUTPUT_PATH/build_status.csv -c $CACHE_DIR