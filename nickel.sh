#!/bin/bash

ARTIFACT_NAME=$1
ARTIFACT_OUT="artifacts/json/$ARTIFACT_NAME.json"
ARTIFACT_IN="artifacts/nickel/$ARTIFACT_NAME.ncl"
CONTRACT="workflow/nickel/artifact_contract.ncl"

# nickel export --format json --output artifacts/json/$ARTIFACT.json workflow/nickel/artifact_contract.ncl artifacts/nickel/$ARTIFACT.ncl
nickel export --format json --output $ARTIFACT_OUT <<< 'let {Artifact, ..} = import "'$CONTRACT'" in ((import "'$ARTIFACT_IN'") | Artifact)'