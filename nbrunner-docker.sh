#!/bin/bash -e
set -euxo pipefail

if [ -z "$SIGNAL_OCEAN_API_KEY" ]; then
  >&2 echo "Error: SIGNAL_OCEAN_API_KEY has not been defined"
  exit 1
else
  echo "Using SIGNAL OCEAN API KEY $SIGNAL_OCEAN_API_KEY"
fi

# esnure html xpath and jq are installed
deb_dependencies="libxml2-utils jq"
if ! dpkg -s $deb_dependencies >/dev/null 2>&1; then
  echo "Installing $deb_dependencies..."
  apt-get update
  apt-get install $deb_dependencies -y --no-install-recommends
fi

python -m venv runner-env
source runner-env/bin/activate

pip install --upgrade pip

pip install notebook jupyter
# Uncomment if you need to manually install
# pip install notebook jupyter plotly matplotlib openpyxl seaborn folium sqlalchemy pandas tqdm --upgrade

pip install --index-url https://test.pypi.org/simple/ --pre --extra-index-url https://pypi.org/simple signal-ocean --no-cache-dir

libs=$(
# indent here-doc to visually align iff you use tabs instead of spaces
# if so change to <<-SCRIPT
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
)

find ./docs -name '*.ipynb' -type f | while read notebook; do
  packages=$(jq -r '.cells[] | select(.cell_type=="code") | .source | add' "$notebook" | grep -Po '^import\s\K[\w_]+|^from\s\K[\w_]+' | uniq)

  installation_candidates=''

  for package in $packages; do
    # could just do the import test but doing this for every package is slow
    # import test is reserved to only find statically linked built-in modules
    package=${package// /}
    if [ -n "$package" ] && [ -z "$(echo "$libs" | grep "^$package")" ] && ! python -c "import $package" > /dev/null 2>&1; then
      installation_candidates="$package $installation_candidates"
    fi
  done

  echo -e "\nFile: $notebook\nCandidates:$installation_candidates\nImported:" $packages

  # try to install the package
  # if that fails fuzzy search closest candidate on PyPi 
  if [ $(wc -w <<< "$installation_candidates") -ge 1 ]; then
    echo "Installing packages:" $installation_candidates "for noteboook: $notebook"
    for candidate in $installation_candidates; do
      pip install $candidate > /dev/null || {
        matched_package=$(./fuzzy_search_pypi_package.sh "$candidate")
        echo -e "$matched_package"
        pip install $matched_package > /dev/null
      }
    done
  fi

  libs="$(echo -e "$libs\n$installation_candidates" | uniq)"

  echo "Converting notebook: $notebook"
  jupyter nbconvert --execute --clear-output "$notebook"
done

# deactivate runner-env
deactivate

# remove runner-env folder
rm -rf runner-env
