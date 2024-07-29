#!/bin/bash

ARTIFACT=$1

nickel export --format json --output artifacts/json/$ARTIFACT.json workflow/nickel/artifact_contract.ncl artifacts/nickel/$ARTIFACT.ncl