ls -LR | grep .ipynb | while read filename; 
do jupyter nbconvert --execute --clear-output docs/examples/jupyter/*/"$filename"; done