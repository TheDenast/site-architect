#!/usr/bin/env bash

PYTHONPATH=$(pwd) python3 -m src.main
cd public && python3 -m http.server 8888
