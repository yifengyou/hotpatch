%global raw_version 0.6.1

Name:           kpatch
Version:        2.0
Release:        3.1.22
Summary:        A Linux dynamic kernel patching infrastructure

License:        GPLv2
URL:            https://github.com/dynup/kpatch
Source0:        https://github.com/dynup/kpatch/archive/%{name}-%{raw_version}.tar.gz

Source1:        os_hotpatch
Source2:        livepatch
Source3:        make_hotpatch

Patch9001:      9001-livepatch-patch-hook-don-t-active-patch-when-insmod.patch
Patch9002:      9002-kpatch-build-support-third-party-module-make-hotpatc.patch
Patch9003:      9003-kpatch-build-support-makefile-not-in-third-party-mod.patch
Patch9004:      9004-create-diff-object-new-static-var-should-be-included.patch
Patch9005:      9005-livepatch-fix-use-THIS-modname-as-the-name-of-ddebug.patch
Patch9006:      9006-create-diff-object-fix-correlate-static-local-variab.patch
Patch9007:      9007-create-diff-object-don-t-create-dynamic-reloc-for-sy.patch
Patch9008:      9008-livepatch-patch-hook-support-force-enable-disable-fu.patch
Patch9009:      9009-kmod-kpatch-build-support-build-patch-for-old-kernel.patch
Patch9010:      9010-kmod-kpatch-build-support-cross-compile-hotpatch-for.patch
Patch9011:      9011-kpatch-build-use-.klp.rela-in-euleros-7.5-kernel.patch
Patch9012:      9012-create-diff-object-create-dynamic-relocs-for-changed.patch
Patch9013:      9013-kmod-kpatch-build-fix-duplicate-symbol-relocation-fo.patch
Patch9014:      9014-create-diff-object-add-dynamic-reloction-for-functio.patch
Patch9015:      9015-create-diff-object-exclude-line-only-change-for-arm6.patch
Patch9016:      9016-kpatch-build-include-secsym-in-kpatch_mark_ignored_s.patch
Patch9017:      9017-support-compile-kpatch-on-aarch64.patch
Patch9018:      9018-support-c-plus-kernel-module.patch
Patch9019:      9019-fix-rodata.str-problem.patch
Patch9020:      0001-Add-__addressable_-to-maybe_discarded_sym.patch
Patch9021:      0002-kmod-patch-fix-patch-linking-with-4.20.patch
Patch9022:      0003-kmod-patch-more-linking-fixes.patch
Patch9023:      9023-kpatch-build-adapt-for-ksymtab-in-4.19-kernel.patch
Patch9024:      9024-support-force-enable-disable-for-kernel-4.19.patch
Patch9025:      9025-kpatch-build-adapt-for-native-compile_env.patch
Patch9026:      9026-add-find_special_section_data_arm64-for-arm64.patch
Patch9027:      9027-fix-ref-static-local-symbol-for-longname-symbol.patch
Patch9028:      9028-add-object-in-kpatch.patch
Patch9029:      0004-create-diff-object-allow-changing-subsections.patch
Patch9030:      9030-kmod-core-fix-compilation-with-CONFIG_HAVE_ARCH_PREL.patch

BuildRequires:  gcc elfutils-libelf-devel uname-build-checks kernel kernel-devel
Requires:       bc tar bash kmod

Provides:       kpatch-runtime
Obsoletes:      kpatch-runtime

%description
kpatch is a Linux dynamic kernel patching infrastructure which allows you to patch
a running kernel without rebooting or restarting any processes. It enables sysadmins
to apply critical security patches to the kernel immediately, without having to wait
for long-running tasks to complete, for users to log off, or for scheduled reboot
windows. It gives more control over uptime without sacrificing security or stability.

%package_help

%prep
%autosetup -n %{name}-%{raw_version} -p1

%build
export CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"
%make_build

%install
%make_install PREFIX=%{_prefix}

install -Dm 0750 -t %{buildroot}/%{_bindir} %{SOURCE1} %{SOURCE2}
install -Dm 0500 -t %{buildroot}/opt/patch_workspace/ %{SOURCE3}
pushd %{buildroot}/opt/patch_workspace
mkdir hotpatch package
popd

%files
%defattr(-,root,root)
%doc COPYING README.md
%{_bindir}/*
%{_prefix}/lib/systemd/system/*
%{_libexecdir}/kpatch
%{_prefix}/sbin/kpatch
%{_datadir}/%{name}/*
%{_sysconfdir}/init/*
%{_bindir}/livepatch
%{_bindir}/os_hotpatch
/opt/patch_workspace/*
%ifarch x86_64
%{_prefix}/lib/kpatch
%endif

%files help
%{_mandir}/man1/*.1.gz

%changelog
* Mon Dec 30 2019 openEuler Buildteam <buildteam@openeuler.org> -2.0-3.1.22
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:change some patch name and delete useless code

* Mon Dec 23 2019 openEuler Buildteam <buildteam@openeuler.org> -2.0-3.1.21
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:modify email adress

* Thu Dec 19 2019 chengquan<chengquan3@huawei.com> -2.0-3.1.20
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:remove useless description

* Thu Nov 28 2019 Yufa Fang<fangyufa1@huawei.com> - 2.0-3.1.19
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix compilation with CONFIG_HAVE_ARCH_PREL32_RELOCATIONS

* Thu Oct 10 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.18
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add security compile flags

* Tue Sep 27 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.17
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:create-diff-object: allow changing subsections

* Tue Sep 24 2019 shenyangyang<shenyangyang4@huawei.com> -2.0-3.1.16
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:revise help package and subpackage

* Mon Aug 26 2019 openEuler Buildteam<buildteam@openeuler.org> -2.0-3.1.15
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:changelog some patch commit message

* Tue Aug 20 2019 openEuler Builteam <buildteam@openeuler.org> -2.0-3.1.14
- Type:NA
- ID:NA
- SUG:NA
- DESC:rewrite spec

* Fri Jul 16 2019 yangbin<robin.yb@huawei.com> - 2.0-3.1.13
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add object in kpatch

* Fri Jul 5 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.12
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:fix ref static local symbol for longname symbol

* Mon Jul 1 2019 Enbo Kang<kangenbo@huawei.com> - 2.0-3.1.11
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:fix security problem

* Tue May 7 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.10
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:change some patch to backport prefix

* Sat Apr 13 2019 hezhanyu<hezhanyu@huawei.com> - 2.0-3.1.9
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:modify private key in sign-modules

* Thu Apr 4 2019 Enbo Kang<kangenbo@huawei.com> - 2.0-3.1.8
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:delete sensitive information

* Thu Mar 28 2019 Enbo Kang<kangenbo@huawei.com> - 2.0-3.1.7
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add RELRO and PIE for create-kpatch-module, create-diff-object, create-klp-module

* Sat Mar 23 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.6
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:upgrade to upstream version  0.6.1

* Thu Mar 7 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.5
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:add find_special_section_data_arm64 for arm64

* Tue Feb 26 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.4
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:add packages required by kpatch and kpatch-runtime

* Mon Feb 25 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.3
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:adapt for native compile_env

* Mon Feb 11 2019 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.2
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:support kernel-4.19

* Thu Dec 20 2018 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.1
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:support c++ kernel module

* Wed Dec 19 2018 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-3.1.0
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:support compile kpatch on aarch64

* Fri Nov 23 2018 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-2.7.2
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:fix some kpatch-build fail cases

* Sat Nov 3 2018 Zhipeng Xie<xiezhipeng1@huawei.com> - 2.0-2.7.1
- Type:enhancement
- ID:NA
- SUG:restart
- DESC:rebase kpatch

* Thu Nov 16 2017 openEuler Builteam <buildteam@openeuler.org> 0.4.0-3
- Package init
