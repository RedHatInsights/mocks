#!/bin/bash

validApps=()

thisDir=$(dirname $0)

for f in $thisDir/*; do
    if [ -d "$f" ]; then validApps+=($(basename $f)); fi
done

found=0

for app in "${validApps[@]}"; do
    if [[ $1 == "$app" ]]; then
        found=1
        echo "starting API for $1"
        python $thisDir/$app/api.py 
        break
    fi
done

if [ "$found" -eq "0" ]; then
    echo "$1: invalid app name, please select one of: ${validApps[@]}"
    exit 1
fi
