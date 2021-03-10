ls -LR | grep .ipynb | while read filename; 
do ~/.local/bin/jupyter nbconvert --execute --clear-output docs/examples/jupyter/*/"$filename"; done