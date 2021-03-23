#!/bin/bash
ls -LR | grep .ipynb | while read filename;
do

if [ -z "${SIGNAL_OCEAN_API_KEY}" ]; 
    then echo 'Error: SIGNAL_OCEAN_API_KEY has not been defined';
    exit 1;
fi

echo "$filename";
jupyter nbconvert --execute --clear-output docs/examples/jupyter/*/"$filename"; 
done
