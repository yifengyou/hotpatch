#!/bin/bash

set -e
gcc --version


sudo apt-get install -y binutils elfutils libelf-dev libunwind-dev \
	rst2pdf build-essential pkg-config

make -C src distclean
make

echo "============================================================="
cd src
echo "Add `pwd` to PATH ,so you can execute cmd directly!"
find ./ -type f -perm 0755 |xargs -i ls -alh {}
echo "============================================================="
echo "All done![$?]"
