#!/bin/bash

echo "Getting GPS data, waiting 1 minute for GPS to find fix"

#sleep 1m

read -p "if led on GPS is flashing, press enter to continue"

config=$(python3 GPSdata3.py arg1 arg2)

echo this is config $config

stellarium $config
