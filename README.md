openEuler内核热补丁使用指南
----------

支持操作系统：

openEuler 20.03 LTS及以上版本

架构支持：

- [x] x86_64
- [x] aarch64
- [ ] risc-v

## 环境准备

安装依赖软件包

```bash
yum install -y make gcc patch bison flex openssl-devel kpatch kpatch-runtime
```

安装当前内核源码和开发包

```bash
yum install -y kernel-source-`uname -r` kernel-debuginfo-`uname -r` kernel-devel-`uname -r`
```

进入热补丁制作目录并准备环境

```bash
cd /opt/patch_workspace
rm -rf kernel-source .config
ln -s /usr/src/linux-`uname -r`/ kernel-source
ln -s /usr/src/linux-`uname -r`/.config .config
ln -s /usr/lib/debug/lib/modules/`uname -r`/vmlinux vmlinux
```

## 制作内核热补丁

支持两种方式制作内核热补丁

### 方法1：直接修改源代码的方式

进入内核源码目录(下面以修改fs/proc/cmdline.c文件为例)

```bash
cd kernel-source
cd fs/proc/
cp cmdline.c cmdline.c.new
```
此处cp操作的后缀.new在后面执行make_hotpatch时会用到

修改cmdline.c.new中的函数

开始制作热补丁

```bash
cd /opt/patch_workspace/
./make_hotpatch -d .new -i cmdline
```

参数  | 说明|
--------- | --------|
-d        |前面cp操作时的唯一后缀名|
-i        |补丁ID，可包括字母和数字|

### 方法2：通过patch文件的方式

```bash
cd /opt/patch_workspace/
./make_hotpatch -i cmdline -p cmdline.patch
```

参数  | 说明|
--------- | --------|
-i        |补丁ID，可包括字母和数字|
-p        |patch文件路径(patch文件必须支持在kernel-source路径下通过patch -p1的方式修改源码)|

补丁制作完成，补丁文件以压缩包的格式存放于/opt/patch_workspace/hotpatch目录下


## 制作第三方模块热补丁


支持两种方式制作第三方模块热补丁

### 方法1：直接修改源代码的方式

进入模块源码目录(下面以https://gitee.com/openeuler/prefetch_tuning模块为例)

```bash
git clone https://gitee.com/openeuler/prefetch_tuning
cd prefetch_tuning
cp prefetch_mod.c prefetch_mod.c.new
```

此处cp操作的后缀.new在后面执行make_hotpatch时会用到

修改prefetch_mod.c.new中的函数

```bash
cd /opt/patch_workspace/
./make_hotpatch -d .new -i testmod -m `pwd`/prefetch_tuning/
```

参数  | 说明|
--------- | --------|
-d        |前面cp操作时的唯一后缀名|
-i        |补丁ID，可包括字母和数字|
-m        |第三方模块源码路径|
-f        |可选，当第三方模块Makefile不在-m指定的源码目录下时，通过该参数指定Makefile的绝对路径|

### 方法2：通过patch文件的方式

```bash
cd /opt/patch_workspace/
./make_hotpatch -i testmod -m `pwd`/prefetch_tuning/ -p testmod.patch
```

参数  | 说明|
--------- | --------|
-i        |补丁ID，可包括字母和数字|
-m        |第三方模块源码路径|
-p        |patch文件路径(patch文件必须支持在-m参数指定的路径下通过patch -p1的方式修改源码)|
-f        |可选，当第三方模块Makefile不在-m指定的源码目录下时，通过该参数指定Makefile的绝对路径|

第三方模块补丁补丁制作完成，补丁文件以压缩包的格式存放于/opt/patch_workspace/hotpatch目录下

## 管理热补丁

### 加载热补丁

```bash
livepatch -l klp_cmdline.tar.gz
```

### 激活热补丁

```bash
livepatch -a cmdline
```

此时热补丁已生效，缺陷函数已被修复。

### 回退热补丁

```bash
livepatch -d cmdline
```

### 卸载热补丁

```bash
livepatch -r cmdline
```

## 编译更新补丁工具

```bash
yum install -y git rpm-build elfutils-libelf-devel uname-build-checks gdb-headless
git clone https://gitee.com/src-openeuler/kpatch.git
mkdir -p ~/rpmbuild/SOURCES/
/bin/cp kpatch/* ~/rpmbuild/SOURCES/
rpmbuild -ba kpatch/kpatch.spec
rpm -Uvh ~/rpmbuild/RPMS/`arch`/kpatch*.rpm
```
