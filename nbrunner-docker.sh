#!/bin/bash -e
set -euxo pipefail

pip install notebook jupyter plotly matplotlib openpyxl seaborn folium sqlalchemy pandas --upgrade
pip install --index-url https://test.pypi.org/simple/ --pre --extra-index-url https://pypi.org/simple signal-ocean

ls -LR | grep .ipynb | while read filename
do

if [ -z "${SIGNAL_OCEAN_API_KEY}" ]
    then echo 'Error: SIGNAL_OCEAN_API_KEY has not been defined'
    exit 1
fi

echo "$filename"
jupyter nbconvert --execute --clear-output docs/examples/jupyter/*/"$filename"
done
