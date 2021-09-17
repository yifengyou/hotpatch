#!/bin/bash

set -xe

libcare-ctl unpatch -p $(pidof foo)

echo "All done![$?]"
