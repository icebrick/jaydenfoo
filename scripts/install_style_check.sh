#!/usr/bin/env bash
# This script is used to install necessary style check tool, including flake8, pre-commit, yapf, isort

# Activate virtual environment
source venv/bin/activate

# Install flake8
echo "********installing flake8********"
pip install flake8
echo "********flake8 installed successfully********"

# Install pre-commit
echo "********installing pre-commit********"
pip install pre-commit
pre-commit install
echo "********pre-commit installed successfully********"

# Install yapf
echo "********installing yapf********"
pip install yapf
echo "********yapf installed successfully********"

# Install isort
echo "********installing isort********"
pip install isort
echo "********isort installed successfully********"

# Check style for all files
echo "********checking all files for the first time********"
pre-commit run --all-files