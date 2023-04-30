#!/bin/bash

# create python env
python -m venv ~/venvs/finance

# Adding lib path to venv
source ~/venvs/finance/bin/activate
package_dir=$(cd $(dirname ${BASH_SOURCE:-$0}) && cd .. && pwd)
python_dir=$(python -c "import site; print(site.getsitepackages())" | cut -d "[" -f 2 | cut -d "]" -f 1 | cut -d "'" -f 2)
pth_file=$python_dir/finance.pth 
echo "Adding finance in $pth_file"
echo "$package_dir" > $pth_file
deactivate

echo "To add in bashrc:"
echo 'echo "source ~/venvs/finance/bin/activate" >> ~/.bashrc'