#!/bin/bash

ls -LR | grep .ipynb | while read filename;
do
env_name=SIGNAL_OCEAN_API_KEY;
apikey=$(printf '%s\n' "${!env_name}");

if [ -z "$apikey" ]; 
    then echo 'Error: SIGNAL_OCEAN_API_KEY has not been defined';
    exit 1;
fi

echo "$filename";
~/.local/bin/jupyter nbconvert --execute --clear-output docs/examples/jupyter/*/"$filename"; 
done
