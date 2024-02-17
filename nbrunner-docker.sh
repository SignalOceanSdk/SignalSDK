#!/bin/bash -e
#set -euxo pipefail

if [ -z "$SIGNAL_OCEAN_API_KEY" ]; then
  >&2 echo "Error: SIGNAL_OCEAN_API_KEY has not been defined"
  #exit 1
fi

#pip install notebook jupyter plotly matplotlib openpyxl seaborn folium sqlalchemy pandas tqdm --upgrade

#pip install --index-url https://test.pypi.org/simple/ --pre --extra-index-url https://pypi.org/simple signal-ocean

function installed_libs() {
python <<SCRIPT | uniq
from itertools import chain
from pathlib import Path
from sysconfig import get_paths

# stdlib, lib and lib64 (the latter 2 contain pip installed packages)
libs = set(v for k, v in get_paths().items() if k in ('stdlib', 'purelib', 'platlib'))

# chain top-level package/module paths
libs_iter = chain(*(Path(lib).glob('*') for lib in libs))

print(*(base.name.split('.')[0] for base in libs_iter), sep='\n')
SCRIPT
}

find . -name *.ipynb | while read notebook; do
  packages=$(jq -r '.cells[] | select(.cell_type=="code") | .source | add' "$notebook" | grep -Po '^import\s\K[\w_]+|^from\s\K[\w_]+' | uniq)

  unset installation_candidates

  for package in $packages;do
    if [ -z "$(installed_libs | grep "^$package")" ]; then
      installation_candidates="$package $installation_candidates"
    fi
  done

  echo -e "\nFile: $notebook\nUninstalled:" $installation_candidates "\nImported:" $packages

  if [ $(wc -w <<< "$installation_candidates") -ge 1 ]; then
    echo "Installing packages:" $installation_candidates "for noteboook: $notebook"
    pip install $installation_candidates
  fi

  #echo "Converting notebook: $notebook"
  #jupyter nbconvert --execute --clear-output "$notebook"
done
