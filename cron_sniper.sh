#!/bin/sh
SHELL=/bin/bash
ENV_PATH=$1
STREAMER=$2

cd $1
# Activate python env
 . ".venv/bin/activate"
./sniper.py $2 >> sniper.log 2>&1
