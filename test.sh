#!/usr/bin/env bash

PYTHONPATH=$(pwd) python3 -m unittest discover -s tests/unit

