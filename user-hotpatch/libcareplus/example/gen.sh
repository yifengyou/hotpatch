#!/bin/bash

set -xe

gcc -S foo.c
gcc -S bar.c
sed -i 's/bar.c/foo.c/' bar.s
kpatch_gensrc --os=rhel6 -i foo.s -i bar.s -o foobar.s --force-global
gcc -o foo foo.s
gcc -o foobar foobar.s -Wl,-q
kpatch_strip --strip foobar foobar.stripped
kpatch_strip --rel-fixup foo foobar.stripped
strip --strip-unneeded foobar.stripped
kpatch_strip --undo-link foo foobar.stripped

str=$(readelf -n foo | grep 'Build ID')
substr=${str##* }
kpatch_make -b $substr foobar.stripped -o foo.kpatch

set +x
echo "========================================="
ls -alh foo.kpatch
file foo.kpatch
echo "========================================="

echo "All done!"
