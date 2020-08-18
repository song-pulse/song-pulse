#! /usr/bin/env bash
set -e

python app/pre_start.py

python -m unittest discover app/tests