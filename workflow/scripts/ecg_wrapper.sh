#!/bin/bash

ECG=$1
CONFIG=$2
PKGLIST=$3
BUILD_STATUS=$4
ARTHASH_LOG=$5
OUTPUT_LOG=$6

python3 $ECG -p $PKGLIST -b $BUILD_STATUS -a $ARTHASH_LOG $CONFIG > $OUTPUT_LOG 2> $OUTPUT_LOG
if [ $? -ne 0 ]
then
    echo "${CONFIG}, `date +%s.%N`, script_crash" >> ${BUILD_STATUS}; exit 0;
fi
