#!/bin/bash

set -xe

libcare-ctl -v patch -p $(pidof foo) ./foo.kpatch

echo "All done![$?]"
