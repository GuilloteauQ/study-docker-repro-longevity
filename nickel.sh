#!/bin/bash

ARTIFACT=$1

nickel export --format json --output artifacts/json/$ARTIFACT.json artifacts/nickel/$ARTIFACT.ncl