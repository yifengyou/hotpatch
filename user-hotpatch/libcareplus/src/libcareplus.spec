Version: 0.1.4
Name: libcareplus
Summary: LibcarePlus tools
Release: 5
Group: Applications/System
License: GPLv2
Url: https://gitee.com/openeuler/libcareplus
Source0: %{name}-%{version}.tar.gz

Patch0001: src-Makefile-install-kpatch_gensrc-into-bindir.patch
Patch0002: 0001-Split-kpatch_storage.c-from-kpatch_user.c.patch
Patch0003: 0002-Split-kpatch_patch.c-from-kpatch_user.c.patch
Patch0004: 0003-cmd_patch-pass-arguments-directly.patch
Patch0005: 0004-travis-use-VM-for-now.patch
Patch0006: 0005-scripts-pkgbuild-add-prepare_env-hook.patch
Patch0007: 0006-pkgbuild-fix-for-non-root-rpmbuild-built-root.patch
Patch0008: 0007-Toil-package-builder.patch
Patch0009: 0008-pkgbuild-use-yumdownloader-if-source-url-is-missing.patch
Patch0010: 0009-execve-abort-on-failure.patch
Patch0011: 0010-Add-test-stage-to-pkgbuild.patch
Patch0012: 0011-glibc-minimal-readme-for-toil-builder.patch
Patch0013: 0012-Fix-kpatch_process_init-kpatch_coroutines_free.patch
Patch0014: 0013-Add-libcare-stresstest.patch
Patch0015: 0014-read-auxv-from-proc-pid-auxv.patch
Patch0016: 0015-add-fail-to-unpatch-test.patch
Patch0017: 0016-Waitpid-for-finished-threads-after-detach.patch
Patch0018: 0017-.gitignore-build-artefacts.patch
Patch0019: 0018-kpatch_storage-put-an-end-to-description-string-load.patch
Patch0020: 0019-Fix-README-files.patch
Patch0021: 0020-include-Create-include-directory-for-header-files.patch
Patch0022: 0021-src-Update-header-file-position.patch
Patch0023: 0022-arch-Create-arch-directory-to-support-multi-arch.patch
Patch0024: 0023-config-configure-out-the-running-arch.patch
Patch0025: 0024-Makefile-Adapt-Makefile-for-different-architectures.patch
Patch0026: 0025-kpatch_parse-Update-asm_directives-for-aarch64.patch
Patch0027: 0026-kpatch_parse-Split-function-parse_ctype.patch
Patch0028: 0027-kpatch_parse-Split-function-init_multilines.patch
Patch0029: 0028-kpatch_parse-Split-function-is_variable_start.patch
Patch0030: 0029-kpatch_parse-Split-function-is_data_def.patch
Patch0031: 0030-kpatch_parse-Split-function-is_function_start.patch
Patch0032: 0031-kpatch_common.h-Factor-out-PAGE_SIZE-marco.patch
Patch0033: 0032-kpatch_coro-Split-function-_UCORO_access_reg.patch
Patch0034: 0033-kpatch_coro-Split-function-get_ptr_guard.patch
Patch0035: 0034-kpatch_coro-Split-function-locate_start_context_symb.patch
Patch0036: 0035-kpatch_patch-Split-function-patch_apply_hunk.patch
Patch0037: 0036-kpatch_elf-Split-function-kpatch_add_jmp_entry.patch
Patch0038: 0037-kpatch_elf-Split-function-kpatch_apply_relocate_add.patch
Patch0039: 0038-kpatch_process-Split-function-object_find_patch_regi.patch
Patch0040: 0039-kpatch_ptrace-Split-function-kpatch_ptrace_waitpid.patch
Patch0041: 0040-kpatch_ptrace-Split-function-copy_regs.patch
Patch0042: 0041-kpatch_ptrace-Split-function-kpatch_execute_remote_f.patch
Patch0043: 0042-kpatch_ptrace-Split-function-kpatch_ptrace_resolve_i.patch
Patch0044: 0043-kpatch_ptrace-Split-function-kpatch_arch_prctl_remot.patch
Patch0045: 0044-kpatch_ptrace-Split-function-kpatch_syscall_remote.patch
Patch0046: 0045-kpatch_ptrace-Split-function-wait_for_mmap.patch
Patch0047: 0046-kpatch_ptrace-Split-function-kpatch_ptrace_kickstart.patch

BuildRequires: elfutils-libelf-devel libunwind-devel gcc systemd

%if 0%{with selinux}
BuildRequires: checkpolicy
BuildRequires: selinux-policy-devel
BuildRequires: /usr/share/selinux/devel/policyhelp
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{with selinux}
Requires:      libcare-selinux = %{version}-%{release}
%endif

%description
LibcarePlus userland tools

%if 0%{with selinux}

%package selinux
Summary: SELinux package for LibcarePlus/QEMU integration
Group: System Environment/Base
Requires(post): selinux-policy-base, policycoreutils
Requires(postun): policycoreutils
%description selinux
This package contains SELinux module required to allow for
LibcarePlus interoperability with the QEMU run by sVirt.

%endif


%package devel
Summary: LibcarePlus development package
Group: System Environment/Development Tools
%description devel
LibcarePlus devel files.


%prep
%setup -q
%autopatch -p1

%build
cd src
sh ./config
cd ../
make -C src
%if 0%{with selinux}
make -C dist/selinux
%endif

%install
%{__rm} -rf %{buildroot}

make -C src install \
        DESTDIR=%{buildroot} \
        bindir=%{_bindir} \
        libexecdir=%{_libexecdir}

%if 0%{with selinux}
make -C dist/selinux install \
        DESTDIR=%{buildroot}
%endif


install -m 0644 -D dist/libcare.service %{buildroot}%{_unitdir}/libcare.service
install -m 0644 -D dist/libcare.socket %{buildroot}%{_unitdir}/libcare.socket
install -m 0644 -D dist/libcare.preset %{buildroot}%{_presetdir}/90-libcare.preset

%pre
/usr/sbin/groupadd libcare -r 2>/dev/null || :
/usr/sbin/usermod -a -G libcare qemu 2>/dev/null || :

%post
%systemd_post libcare.service
%systemd_post libcare.socket

if [ $1 -eq 1 ]; then
        # First install
        systemctl start libcare.socket
fi
if [ $1 -eq 2 ]; then
        # Upgrade. Just stop it, we will be reactivated
        # by a connect to /run/libcare.sock
        systemctl stop libcare.service
fi

%preun
%systemd_preun libcare.socket
%systemd_preun libcare.service

%postun
%systemd_postun libcare.service
%systemd_postun libcare.socket

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/libcare-ctl
%{_bindir}/libcare-client
%{_unitdir}/libcare.service
%{_unitdir}/libcare.socket
%{_presetdir}/90-libcare.preset

%files devel
%defattr(-,root,root)
%{_bindir}/libcare-cc
%{_bindir}/libcare-patch-make
%{_bindir}/kpatch_gensrc
%{_bindir}/kpatch_strip
%{_bindir}/kpatch_make

%if 0%{with selinux}

%files selinux
%defattr(-,root,root,-)
%attr(0600,root,root) %{_datadir}/selinux/packages/libcare.pp

%post selinux
. /etc/selinux/config
FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

/usr/sbin/semodule -i %{_datadir}/selinux/packages/libcare.pp

# Load the policy if SELinux is enabled
if ! /usr/sbin/selinuxenabled; then
    # Do not relabel if selinux is not enabled
    exit 0
fi

/usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null

rm -f ${FILE_CONTEXT}.pre

exit 0

%postun selinux
if [ $1 -eq 0 ]; then
    . /etc/selinux/config
    FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
    cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

    # Remove the module
    /usr/sbin/semodule -n -r libcare > /dev/null 2>&1

    /usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null
fi
exit 0

%endif

%changelog
* Sat Aug 21 2021 caodongxia <caodongxia@huawei.com> - 0.1.4-5
- fixes uninstall warning

* Tue Jun 08 2021 wulei <wulei80@huawei.com> - 0.1.4-4
- fixes failed: gcc: command not found

* Tue Feb 09 2021 Jiajie Li <lijiajie11@huawei.com> - 0.1.4-3
- Add basic support libcareplus on aarch64

* Mon Dec 28 2020 sunguoshuai <sunguoshuai@huawei.com> - 0.1.4-2
- Del the {dist} in release.

* Tue Dec 8 2020 Ying Fang <fangying1@huawei.com>
- Init the libcareplus package spec
