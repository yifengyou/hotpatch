使用指南
----------

## 制作内核热补丁

### 环境准备

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

支持两种方式制作内核热补丁

### 方法1：直接修改源代码的方式

进入内核源码目录(下面以修改fs/proc/cmdline.c文件为例)

```bash
cd kernel-source
cd fs/proc/
cp cmdline.c cmdline.c.new
```

修改cmdline.c.new中的函数

开始制作热补丁

```bash
./make_hotpatch -d .new -i cmdline
```

参数说明：

-d 后面跟上前面cp操作时的唯一后缀名。

-i 后跟补丁ID，可包括字母和数字。

### 方法2：通过patch文件的方式

```bash
./make_hotpatch -i cmdline -p cmdline.patch
```

参数说明：

-p patch文件路径

补丁制作完成，补丁文件以压缩包的格式存放于/opt/patch_workspace/hotpatch目录下


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

