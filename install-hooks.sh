#!/usr/bin/env bash

# define hooks and virtualenv directory
HOOKS_DIR=`git rev-parse --git-dir`/hooks
HOOKS_VENV_DIR=${HOOKS_DIR}/hooks_venv

# work on the virtualenv
hash virtualenv >> /dev/null || pip install virtualenv
virtualenv -p `which python3.6` ${HOOKS_VENV_DIR}  # Note: python below 3.6.5 will not work
source ${HOOKS_VENV_DIR}/bin/activate

# install the python requirements and yelp pre-commit to the project
pip install -r hooks/requirements.txt
pre-commit install -f

# wrapper the yelp pre-commit to the virtualenv for the hooks
mv ${HOOKS_DIR}/pre-commit ${HOOKS_DIR}/yelp-pre-commit.sh
cp hooks/pre-commit ${HOOKS_DIR}/
chmod +x ${HOOKS_DIR}/pre-commit

echo "pre-commit hook has been installed successfully"
