#!/bin/bash

set -e
gcc --version


sudo apt-get install -y binutils elfutils libelf-dev libunwind-dev \
	rst2pdf build-essential pkg-config

[ -d libcareplus-0.1.4 ] && rm -rf libcareplus-0.1.4
tar -xvf libcareplus-0.1.4.tar.gz && cd libcareplus-0.1.4

for p in `ls ../patches/*.patch`;do
	patch -p1 < ${p}
done
echo "Patch done!"

echo `uname -m` > src/arch.desc
make -C src distclean
make

echo "============================================================="
cd src
echo "Add `pwd` to PATH ,so you can execute cmd directly!"
find ./ -type f -perm 0755 |xargs -i ls -alh {}
echo "============================================================="
echo "All done![$?]"
