#!/bin/bash

ls -LR | grep .ipynb | while read filename;
do
env_name=SIGNAL_OCEAN_API_KEY;
apikey=$(printf '%s\n' "${!env_name}");
echo $apikey

if [ -z "$apikey" ]; 
    then echo 'Error: SIGNAL_OCEAN_API_KEY has not been defined';
    exit 1;
fi

echo "$filename";

sed -i 's/subscription_key = \\"\\"/subscription_key = \\"'$apikey'\\"/' docs/examples/jupyter/*/"$filename";
sed -i "s/subscription_key = ''/subscription_key = '$apikey'/" docs/examples/jupyter/*/"$filename";
sed -i "s/signal_ocean_api_key = ''/signal_ocean_api_key = '$apikey'/" docs/examples/jupyter/*/"$filename";
sed -i "s/signal_ocean_api_key = 'NotValid'/signal_ocean_api_key = '$apikey'/" docs/examples/jupyter/*/"$filename";

~/.local/bin/jupyter nbconvert --execute --clear-output docs/examples/jupyter/*/"$filename"; 
done