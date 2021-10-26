#!/bin/bash
rm -rf kpatch_compile_env
yum install -y strace vim git rpm-build bc elfutils-libelf-devel gdb-headless make gcc patch bison flex openssl-devel kernel-source-`uname -r` kernel-debuginfo-`uname -r` kernel-devel-`uname -r` --installroot=`pwd`/kpatch_compile_env/
mkdir -p kpatch_compile_env/kpatch
/bin/cp * kpatch_compile_env/kpatch/
cat > kpatch_compile_env/installkpatch.sh <<EOF
#!/bin/bash
mkdir -p ~/rpmbuild/SOURCES/
/bin/cp kpatch/* ~/rpmbuild/SOURCES/
rpmbuild -ba kpatch/kpatch.spec
rpm -Uvh ~/rpmbuild/RPMS/`arch`/kpatch*.rpm
cd /opt/patch_workspace
rm -rf kernel-source .config
ln -s /usr/src/linux-`uname -r`/ kernel-source
ln -s /usr/src/linux-`uname -r`/.config .config
ln -s /usr/lib/debug/lib/modules/`uname -r`/vmlinux vmlinux
rm -rf /dev/null
mknod /dev/null c 1 3
rm -rf /dev/zero
mknod /dev/zero c 1 5
rm -rf /dev/random
mknod /dev/random c 1 8
rm -rf /dev/tty
mknod /dev/tty c 5 0
EOF
chmod a+x kpatch_compile_env/installkpatch.sh
chroot kpatch_compile_env /installkpatch.sh
cat > kpatch_compile_env/chroot.sh <<EOF
mount -t proc proc \$(dirname \$0)/proc
chroot \$(dirname \$0)
EOF
cat > kpatch_compile_env/unchroot.sh <<EOF
umount \$(dirname \$0)/proc
EOF
cat > kpatch_compile_env/usr/bin/openEuler_history<<EOF
#!/bin/bash
EOF
chmod a+x kpatch_compile_env/chroot.sh
chmod a+x kpatch_compile_env/unchroot.sh
chmod a+x kpatch_compile_env/usr/bin/openEuler_history
tar -czf kpatch_compile_env.tar.gz kpatch_compile_env
rm -rf kpatch_compile_env
