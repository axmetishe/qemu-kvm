%global SLOF_gittagdate 20170724
%global SLOF_gittagcommit 89f519f

%global have_usbredir 1
%global have_spice    1
%global have_opengl   1
%global have_fdt      0
%global have_gluster  1
%global have_kvm_setup 0
%global have_memlock_limits 0

%ifnarch %{ix86} x86_64
    %global have_usbredir 0
%endif

%ifnarch s390x
    %global have_librdma 1
%else
    %global have_librdma 0
%endif

%ifarch %{ix86}
    %global kvm_target    i386
%endif
%ifarch x86_64
    %global kvm_target    x86_64
%else
    %global have_spice   0
    %global have_opengl  0
    %global have_gluster 0
%endif
%ifarch %{power64}
    %global kvm_target    ppc64
    %global have_fdt     1
    %global have_kvm_setup 1
    %global have_memlock_limits 1
%endif
%ifarch s390x
    %global kvm_target    s390x
%endif
%ifarch ppc
    %global kvm_target    ppc
    %global have_fdt     1
%endif
%ifarch aarch64
    %global kvm_target    aarch64
    %global have_fdt     1
%endif

#Versions of various parts:

%global requires_all_modules                                     \
Requires: %{name}-block-curl = %{epoch}:%{version}-%{release}    \
%if %{have_gluster}                                              \
Requires: %{name}-block-gluster = %{epoch}:%{version}-%{release} \
%endif                                                           \
Requires: %{name}-block-iscsi = %{epoch}:%{version}-%{release}   \
Requires: %{name}-block-rbd = %{epoch}:%{version}-%{release}     \
Requires: %{name}-block-ssh = %{epoch}:%{version}-%{release}

%define version 4.2.0
Summary: QEMU is a machine emulator and virtualizer
Name: qemu-kvm
Version: %{version}
Release: 64%{?dist}.2
# Epoch because we pushed a qemu-1.0 package. AIUI this can't ever be dropped
Epoch: 15
License: GPLv2 and GPLv2+ and CC-BY
Group: Development/Tools
URL: http://www.qemu.org/
ExclusiveArch: x86_64 %{power64} aarch64 s390x


Source0: https://wiki.qemu.org/download/qemu-%{version}.tar.xz

# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf
Source10: qemu-guest-agent.service
Source11: 99-qemu-guest-agent.rules
Source12: bridge.conf
Source13: qemu-ga.sysconfig
Source21: kvm-setup
Source22: kvm-setup.service
Source23: 85-kvm.preset
Source26: vhost.conf
Source27: kvm.conf
Source28: 95-kvm-memlock.conf
Source30: kvm-s390x.conf
Source31: kvm-x86.conf
Source32: qemu-pr-helper.service
Source33: qemu-pr-helper.socket
Source34: 81-kvm-rhel.rules
Source35: udev-kvm-check.c

Patch0001: 0001-Initial-redhat-build.patch

BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: which
BuildRequires: gnutls-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libtool
BuildRequires: libaio-devel
BuildRequires: rsync
BuildRequires: python3-devel
# qemu 4.0: Used by test suite ./scripts/tap-driver.pl
BuildRequires: perl-Test-Harness
# Required for making python shebangs versioned
BuildRequires: /usr/bin/pathfix.py
BuildRequires: pciutils-devel
BuildRequires: libiscsi-devel
BuildRequires: ncurses-devel
BuildRequires: libattr-devel
BuildRequires: libusbx-devel >= 1.0.22
%if %{have_usbredir}
BuildRequires: usbredir-devel >= 0.7.1
%endif
BuildRequires: texinfo
%if %{have_spice}
BuildRequires: spice-protocol >= 0.12.12
BuildRequires: spice-server-devel >= 0.12.8
BuildRequires: libcacard-devel
# For smartcard NSS support
BuildRequires: nss-devel
%endif
BuildRequires: libseccomp-devel >= 2.3.0
# For network block driver
BuildRequires: libcurl-devel
BuildRequires: libssh-devel
BuildRequires: librados-devel
BuildRequires: librbd-devel
%if %{have_gluster}
# For gluster block driver
BuildRequires: glusterfs-api-devel >= 3.6.0
BuildRequires: glusterfs-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-libs-devel
# For Braille device support
BuildRequires: brlapi-devel
# For test suite
BuildRequires: check-devel
# For virtfs
BuildRequires: libcap-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# Documentation requirement
BuildRequires: perl-podlators
BuildRequires: texinfo
BuildRequires: python3-sphinx
# For rdma
%if 0%{?have_librdma}
BuildRequires: rdma-core-devel
%endif
%if %{have_fdt}
BuildRequires: libfdt-devel >= 1.4.3
%endif
# iasl and cpp for acpi generation (not a hard requirement as we can use
# pre-compiled files, but it's better to use this)
%ifarch %{ix86} x86_64
BuildRequires: iasl
BuildRequires: cpp
%endif
# For compressed guest memory dumps
BuildRequires: lzo-devel snappy-devel
# For NUMA memory binding
%ifnarch s390x
BuildRequires: numactl-devel
%endif
BuildRequires: libgcrypt-devel
# qemu-pr-helper multipath support (requires libudev too)
BuildRequires: device-mapper-multipath-devel
BuildRequires: systemd-devel
# used by qemu-bridge-helper and qemu-pr-helper
BuildRequires: libcap-ng-devel

BuildRequires: diffutils
%ifarch x86_64
BuildRequires: libpmem-devel
Requires: libpmem
BuildRequires: jemalloc-devel
%endif

# qemu-keymap
BuildRequires: pkgconfig(xkbcommon)

# For s390-pgste flag
%ifarch s390x
BuildRequires: binutils >= 2.27-16
%endif

%if %{have_opengl}
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(gbm)
Requires:      mesa-libGL
Requires:      mesa-libEGL
Requires:      mesa-dri-drivers
%endif

%{requires_all_modules}

%define qemudocdir %{_docdir}/%{name}

%description
qemu-kvm is an open source virtualizer that provides hardware
emulation for the KVM hypervisor. qemu-kvm acts as a virtual
machine monitor together with the KVM kernel modules, and emulates the
hardware for a full system such as a PC and its associated peripherals.


%package -n qemu-kvm-core
Summary: qemu-kvm core components
Requires: qemu-img = %{epoch}:%{version}-%{release}
%ifarch %{ix86} x86_64
Requires: seabios-bin >= 1.10.2-1
Requires: sgabios-bin
Requires: edk2-ovmf
%endif
%ifarch aarch64
Requires: edk2-aarch64
%endif

%ifnarch aarch64 s390x
Requires: seavgabios-bin >= 1.10.2-1
Requires: ipxe-roms-qemu >= 20170123-1
%endif
%ifarch %{power64}
Requires: SLOF >= %{SLOF_gittagdate}-1.git%{SLOF_gittagcommit}
%endif
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: libseccomp >= 2.3.0
# For compressed guest memory dumps
Requires: lzo snappy
%if %{have_gluster}
Requires: glusterfs-api >= 3.6.0
%endif
%if %{have_kvm_setup}
Requires(post): systemd-units
    %ifarch %{power64}
Requires: powerpc-utils
    %endif
%endif
Requires: libusbx >= 1.0.19
%if %{have_usbredir}
Requires: usbredir >= 0.7.1
%endif

%description -n qemu-kvm-core
qemu-kvm is an open source virtualizer that provides hardware
emulation for the KVM hypervisor. qemu-kvm acts as a virtual
machine monitor together with the KVM kernel modules, and emulates the
hardware for a full system such as a PC and its associated peripherals.


%package -n qemu-img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools

%description -n qemu-img
This package provides a command line tool for manipulating disk images.

%package -n qemu-kvm-common
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n qemu-kvm-common
qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides documentation and auxiliary programs used with qemu-kvm.


%package -n qemu-guest-agent
Summary: QEMU guest agent
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n qemu-guest-agent
qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%package tests
Summary: tests for the qemu-kvm package
Requires: %{name} = %{epoch}:%{version}-%{release}

%define testsdir %{_libdir}/%{name}/tests-src

%description tests
The qemu-kvm-tests rpm contains tests that can be used to verify
the functionality of the installed qemu-kvm package

Install this package if you want access to the avocado_qemu
tests, or qemu-iotests.

%package  block-curl
Summary: QEMU CURL block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.


%if %{have_gluster}
%package  block-gluster
Summary: QEMU Gluster block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-gluster
This package provides the additional Gluster block driver for QEMU.

Install this package if you want to access remote Gluster storage.
%endif


%package  block-iscsi
Summary: QEMU iSCSI block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.


%package  block-rbd
Summary: QEMU Ceph/RBD block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-rbd
This package provides the additional Ceph/RBD block driver for QEMU.

Install this package if you want to access remote Ceph volumes
using the rbd protocol.


%package  block-ssh
Summary: QEMU SSH block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-ssh
This package provides the additional SSH block driver for QEMU.

Install this package if you want to access remote disks using
the Secure Shell (SSH) protocol.


%prep
%setup -q -n qemu-%{version}
%autopatch -p1
# https://fedoraproject.org/wiki/Changes/Make_ambiguous_python_shebangs_error
# Fix all Python shebangs recursively in .
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# Need to list files that do not match ^[a-zA-Z0-9_]+\.py$ explicitly!
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" scripts/qemu-trace-stap

%build
%global buildarch %{kvm_target}-softmmu

# --build-id option is used for giving info to the debug packages.
buildldflags="VL_LDFLAGS=-Wl,--build-id"

%global block_drivers_list qcow2,raw,file,host_device,nbd,iscsi,rbd,blkdebug,luks,null-co,nvme,copy-on-read,throttle

%if 0%{have_gluster}
    %global block_drivers_list %{block_drivers_list},gluster
%endif

./configure  \
 --prefix="%{_prefix}" \
 --libdir="%{_libdir}" \
 --sysconfdir="%{_sysconfdir}" \
 --interp-prefix=%{_prefix}/qemu-%M \
 --localstatedir="%{_localstatedir}" \
 --docdir="%{qemudocdir}" \
 --libexecdir="%{_libexecdir}" \
 --extra-ldflags="-Wl,--build-id -Wl,-z,relro -Wl,-z,now" \
 --extra-cflags="%{optflags}" \
 --with-pkgversion="%{name}-%{version}-%{release}" \
 --with-confsuffix=/"%{name}" \
 --firmwarepath=%{_prefix}/share/qemu-firmware \
%if 0%{have_fdt}
  --enable-fdt \
%else
  --disable-fdt \
 %endif
%if 0%{have_gluster}
  --enable-glusterfs \
%else
  --disable-glusterfs \
%endif
  --enable-guest-agent \
%ifnarch s390x
  --enable-numa \
%else
  --disable-numa \
%endif
  --enable-rbd \
%if 0%{have_librdma}
  --enable-rdma \
%else
  --disable-rdma \
%endif
  --enable-seccomp \
%if 0%{have_spice}
  --enable-spice \
  --enable-smartcard \
%else
  --disable-spice \
  --disable-smartcard \
%endif
%if 0%{have_opengl}
  --enable-opengl \
%else
  --disable-opengl \
%endif
%if 0%{have_usbredir}
  --enable-usb-redir \
%else
  --disable-usb-redir \
%endif
  --disable-tcmalloc \
%ifarch x86_64
  --enable-libpmem \
  --enable-jemalloc \
%else
  --disable-libpmem \
%endif
  --enable-vhost-user \
  --python=%{__python3} \
  --target-list="%{buildarch}" \
  --block-drv-rw-whitelist=%{block_drivers_list} \
  --audio-drv-list= \
  --block-drv-ro-whitelist=vmdk,vhdx,vpc,https,ssh \
  --with-coroutine=ucontext \
  --tls-priority=NORMAL \
  --disable-bluez \
  --disable-brlapi \
  --disable-cap-ng \
  --enable-coroutine-pool \
  --enable-curl \
  --disable-curses \
  --disable-debug-tcg \
  --enable-docs \
  --disable-gtk \
  --enable-kvm \
  --enable-libiscsi \
  --disable-libnfs \
  --disable-libssh \
  --enable-libusb \
  --disable-bzip2 \
  --enable-linux-aio \
  --disable-live-block-migration \
  --enable-lzo \
  --enable-pie \
  --disable-qom-cast-debug \
  --disable-sdl \
  --enable-snappy \
  --disable-sparse \
  --disable-strip \
  --enable-tpm \
  --enable-trace-backend=dtrace \
  --disable-vde \
  --disable-vnc-jpeg \
  --disable-vte \
  --enable-vnc-png \
  --enable-vnc-sasl \
  --enable-werror \
  --disable-xen \
  --disable-xfsctl \
  --enable-gnutls \
  --enable-gcrypt \
  --disable-nettle \
  --enable-attr \
  --disable-bsd-user \
  --disable-cocoa \
  --enable-debug-info \
  --disable-guest-agent-msi \
  --disable-hax \
  --disable-tcmalloc \
  --disable-linux-user \
  --enable-modules \
  --disable-netmap \
  --disable-replication \
  --enable-system \
  --enable-tools \
  --disable-user \
  --enable-vhost-net \
  --enable-vhost-vsock \
  --enable-vnc \
  --enable-mpath \
  --disable-virglrenderer \
  --disable-xen-pci-passthrough \
  --enable-tcg \
  --with-git=git \
  --disable-sanitizers \
  --disable-hvf \
  --disable-whpx \
  --disable-malloc-trim \
  --disable-membarrier \
  --disable-vhost-crypto \
  --disable-libxml2 \
  --enable-capstone \
  --disable-git-update \
  --disable-crypto-afalg \
  --disable-bochs \
  --disable-cloop \
  --disable-dmg \
  --disable-qcow1 \
  --disable-vdi \
  --disable-vvfat \
  --disable-qed \
  --disable-parallels \
  --disable-vxhs \
  --disable-sheepdog

make V=1 %{?_smp_mflags} $buildldflags

# Setup back compat qemu-kvm binary
%{__python3} scripts/tracetool.py --backend dtrace --format stap --group=all \
  --binary %{_libexecdir}/qemu-kvm --target-name %{kvm_target} \
  --target-type system --probe-prefix \
  qemu.kvm trace-events-all > qemu-kvm.stp

%{__python3} scripts/tracetool.py --backend dtrace --format simpletrace-stap \
  --group=all --binary %{_libexecdir}/qemu-kvm --target-name %{kvm_target} \
  --target-type system --probe-prefix \
  qemu.kvm trace-events-all > qemu-kvm-simpletrace.stp

cp -a %{kvm_target}-softmmu/qemu-system-%{kvm_target} qemu-kvm

gcc %{SOURCE6} $RPM_OPT_FLAGS $RPM_LD_FLAGS -o ksmctl
gcc %{SOURCE35} $RPM_OPT_FLAGS $RPM_LD_FLAGS -o udev-kvm-check

%install
%define _udevdir %(pkg-config --variable=udevdir udev)
%define _udevrulesdir %{_udevdir}/rules.d

install -D -p -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/ksm.service
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
install -D -p -m 0755 ksmctl $RPM_BUILD_ROOT%{_libexecdir}/ksmctl

install -D -p -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}/ksmtuned.service
install -D -p -m 0755 %{SOURCE8} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
install -D -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf
install -D -p -m 0644 %{SOURCE26} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/vhost.conf
%ifarch s390x
    install -D -p -m 0644 %{SOURCE30} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/kvm.conf
%else
%ifarch %{ix86} x86_64
    install -D -p -m 0644 %{SOURCE31} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/kvm.conf
%else
    install -D -p -m 0644 %{SOURCE27} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/kvm.conf
%endif
%endif

mkdir -p $RPM_BUILD_ROOT%{_bindir}/
mkdir -p $RPM_BUILD_ROOT%{_udevrulesdir}/
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

# Create new directories and put them all under tests-src
mkdir -p $RPM_BUILD_ROOT%{testsdir}/tests/
mkdir -p $RPM_BUILD_ROOT%{testsdir}/tests/acceptance
mkdir -p $RPM_BUILD_ROOT%{testsdir}/tests/qemu-iotests
mkdir -p $RPM_BUILD_ROOT%{testsdir}/scripts
mkdir -p $RPM_BUILD_ROOT%{testsdir}/scripts/qmp

install -p -m 0755 udev-kvm-check $RPM_BUILD_ROOT%{_udevdir}
install -p -m 0644 %{SOURCE34} $RPM_BUILD_ROOT%{_udevrulesdir}

install -m 0644 scripts/dump-guest-memory.py \
                $RPM_BUILD_ROOT%{_datadir}/%{name}

# Install avocado_qemu tests
cp -R tests/acceptance/* $RPM_BUILD_ROOT%{testsdir}/tests/acceptance/

# Install qemu.py and qmp/ scripts required to run avocado_qemu tests
install -p -m 0644 python/qemu/machine.py $RPM_BUILD_ROOT%{testsdir}/scripts/
cp -R scripts/qmp/* $RPM_BUILD_ROOT%{testsdir}/scripts/qmp
install -p -m 0755 tests/Makefile.include $RPM_BUILD_ROOT%{testsdir}/tests/

# Install qemu-iotests
cp -R tests/qemu-iotests/* $RPM_BUILD_ROOT%{testsdir}/tests/qemu-iotests/
# Avoid ambiguous 'python' interpreter name
find $RPM_BUILD_ROOT%{testsdir}/tests/qemu-iotests/* -maxdepth 1 -type f -exec sed -i -e '1 s/python/python3/' {} \;
find $RPM_BUILD_ROOT%{testsdir}/scripts/qmp/* -maxdepth 1 -type f -exec sed -i -e '1 s/python/python3/' {} \;

make DESTDIR=$RPM_BUILD_ROOT \
    sharedir="%{_datadir}/%{name}" \
    datadir="%{_datadir}/%{name}" \
    install

mkdir -p $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset

# Install qemu-guest-agent service and udev rules
install -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/qemu-ga.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/qemu-ga
install -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevrulesdir}

# - the fsfreeze hook script:
install -D --preserve-timestamps \
            scripts/qemu-guest-agent/fsfreeze-hook \
            $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ga/fsfreeze-hook

# - the directory for user scripts:
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ga/fsfreeze-hook.d

# - and the fsfreeze script samples:
mkdir --parents $RPM_BUILD_ROOT%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
install --preserve-timestamps --mode=0644 \
             scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample \
             $RPM_BUILD_ROOT%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/

# - Install dedicated log directory:
mkdir -p -v $RPM_BUILD_ROOT%{_localstatedir}/log/qemu-ga/

mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -c -m 0755  qemu-ga ${RPM_BUILD_ROOT}%{_bindir}/qemu-ga

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m 0644  docs/built/interop/qemu-ga.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/


install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_libexecdir}/
install -m 0644 qemu-kvm.stp $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/
install -m 0644 qemu-kvm-simpletrace.stp $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/

rm $RPM_BUILD_ROOT%{_bindir}/qemu-system-%{kvm_target}
rm $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/qemu-system-%{kvm_target}.stp
rm $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/qemu-system-%{kvm_target}-simpletrace.stp

# Install simpletrace
install -m 0755 scripts/simpletrace.py $RPM_BUILD_ROOT%{_datadir}/%{name}/simpletrace.py
# Avoid ambiguous 'python' interpreter name
sed -i -e '1 s/python/python3/' $RPM_BUILD_ROOT%{_datadir}/%{name}/simpletrace.py
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/tracetool
install -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/%{name}/tracetool scripts/tracetool/*.py
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/tracetool/backend
install -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/%{name}/tracetool/backend scripts/tracetool/backend/*.py
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/tracetool/format
install -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/%{name}/tracetool/format scripts/tracetool/format/*.py

mkdir -p $RPM_BUILD_ROOT%{qemudocdir}
install -p -m 0644 -t ${RPM_BUILD_ROOT}%{qemudocdir} Changelog COPYING COPYING.LIB LICENSE docs/interop/qmp-spec.txt
chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man8/*

install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/%{name}.conf

# Provided by package openbios
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-ppc
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc32
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/slof.bin

# Remove unpackaged files.
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/palcode-clipper
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/petalogix*.dtb
#rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bamboo.dtb
#rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/ppc_rom.bin
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/s390-zipl.rom
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/u-boot.e500
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/qemu_vga.ndrv
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/skiboot.lid
#
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/s390-ccw.img
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/hppa-firmware.img
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/canyonlands.dtb
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/u-boot-sam460-20100605.bin

%ifarch s390x
    # Use the s390-ccw.img that we've just built, not the pre-built one
    install -m 0644 pc-bios/s390-ccw/s390-ccw.img $RPM_BUILD_ROOT%{_datadir}/%{name}/
%else
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/s390-netboot.img
%endif

%ifnarch %{power64}
    rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/spapr-rtas.bin
%endif

%ifnarch x86_64
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/kvmvapic.bin
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/linuxboot.bin
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/multiboot.bin
%endif

# Remove sparc files
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/QEMU,tcx.bin
#rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/QEMU,cgthree.bin

# Remove ivshmem example programs
#rm -rf ${RPM_BUILD_ROOT}%{_bindir}/ivshmem-client
#rm -rf ${RPM_BUILD_ROOT}%{_bindir}/ivshmem-server

# Remove efi roms
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/efi*.rom

# Provided by package ipxe
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/pxe*rom
# Provided by package vgabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/bios*.bin
# Provided by package sgabios
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{name}/sgabios.bin

# the pxe gpxe images will be symlinks to the images on
# /usr/share/ipxe, as QEMU doesn't know how to look
# for other paths, yet.
pxe_link() {
    ln -s ../ipxe.efi/$2.rom %{buildroot}%{_datadir}/%{name}/efi-$1.rom
}

%ifnarch aarch64 s390x
pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000
pxe_link eepro100 80861209
pxe_link e1000e 808610d3
pxe_link vmxnet3 15ad07b0
%endif

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

%ifnarch aarch64 s390x
  rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
  rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
  rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
  rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
  rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
  rom_link ../seavgabios/vgabios-virtio.bin vgabios-virtio.bin
  rom_link ../seavgabios/vgabios-ramfb.bin vgabios-ramfb.bin
  rom_link ../seavgabios/vgabios-bochs-display.bin vgabios-bochs-display.bin
  rom_link ../seavgabios/vgabios-ati.bin vgabios-ati.bin
%endif
%ifarch x86_64
  rom_link ../seabios/bios.bin bios.bin
  rom_link ../seabios/bios-256k.bin bios-256k.bin
  rom_link ../sgabios/sgabios.bin sgabios.bin
%endif

%if 0%{have_kvm_setup}
    install -D -p -m 755 %{SOURCE21} $RPM_BUILD_ROOT%{_prefix}/lib/systemd/kvm-setup
    install -D -p -m 644 %{SOURCE22} $RPM_BUILD_ROOT%{_unitdir}/kvm-setup.service
    install -D -p -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_presetdir}/85-kvm.preset
%endif

%if 0%{have_memlock_limits}
    install -D -p -m 644 %{SOURCE28} $RPM_BUILD_ROOT%{_sysconfdir}/security/limits.d/95-kvm-memlock.conf
%endif

# Install rules to use the bridge helper with libvirt's virbr0
install -D -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/bridge.conf

# Install qemu-pr-helper service
install -m 0644 %{_sourcedir}/qemu-pr-helper.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/qemu-pr-helper.socket %{buildroot}%{_unitdir}

find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

# We need to make the block device modules executable else
# RPM won't pick up their dependencies.
chmod +x $RPM_BUILD_ROOT%{_libdir}/qemu-kvm/block-*.so

%check
export DIFF=diff; make check V=1
pushd tests/qemu-iotests
./check -v -raw 001 002 004 005 008 009 010 011 012 021 025 032 033 048 052 063 077 086 101 106 120 140 143 145 150 159 160 162 170 171 175 184 221 226 ||:
./check -v -qcow2 001 002 004 005 008 009 010 011 012 017 018 019 020 021 024 025 027 028 029 032 033 034 035 037 038 042 046 047 048 050 052 053 058 062 063 066 068 069 072 073 074 086 087 089 090 095 098 102 103 105 107 108 110 111 120 127 133 134 138 140 141 143 144 145 150 154 156 158 159 162 170 177 179 182 184 188 190 195 204 209 217 226 ||:
popd

%post -n qemu-kvm-core
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
%udev_rules_update
sh %{_sysconfdir}/sysconfig/modules/kvm.modules &> /dev/null || :
    udevadm trigger --subsystem-match=misc --sysname-match=kvm --action=add || :
%if %{have_kvm_setup}
    systemctl daemon-reload # Make sure it sees the new presets and unitfile
    %systemd_post kvm-setup.service
    if systemctl is-enabled kvm-setup.service > /dev/null; then
        systemctl start kvm-setup.service
    fi
%endif

%post -n qemu-kvm-common
%systemd_post ksm.service
%systemd_post ksmtuned.service

getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
  -c "qemu user" qemu

%preun -n qemu-kvm-common
%systemd_preun ksm.service
%systemd_preun ksmtuned.service

%postun -n qemu-kvm-common
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service

%global qemu_kvm_files \
%{_libexecdir}/qemu-kvm \
%{_datadir}/systemtap/tapset/qemu-kvm.stp \
%{_datadir}/%{name}/trace-events-all \
%{_datadir}/systemtap/tapset/qemu-kvm-simpletrace.stp \
%{_datadir}/%{name}/systemtap/script.d/qemu_kvm.stp \
%{_datadir}/%{name}/systemtap/conf.d/qemu_kvm.conf

%files
# Deliberately empty


%files -n qemu-kvm-common
%defattr(-,root,root)
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README
%doc %{qemudocdir}/qemu-doc.html
%doc %{qemudocdir}/COPYING
%doc %{qemudocdir}/COPYING.LIB
%doc %{qemudocdir}/LICENSE
%doc %{qemudocdir}/README.systemtap
%doc %{qemudocdir}/qmp-spec.txt
%doc %{qemudocdir}/qemu-doc.txt
%doc %{qemudocdir}/qemu-ga-ref.html
%doc %{qemudocdir}/qemu-ga-ref.txt
%doc %{qemudocdir}/qemu-qmp-ref.html
%doc %{qemudocdir}/qemu-qmp-ref.txt
%{_mandir}/man7/qemu-qmp-ref.7*
%{_bindir}/qemu-keymap
%{_bindir}/qemu-pr-helper
%{_unitdir}/qemu-pr-helper.service
%{_unitdir}/qemu-pr-helper.socket
%{_mandir}/man7/qemu-ga-ref.7*

%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/keymaps/
%{_mandir}/man1/%{name}.1*
%{_mandir}/man7/qemu-block-drivers.7*
%attr(4755, -, -) %{_libexecdir}/qemu-bridge-helper
%config(noreplace) %{_sysconfdir}/sasl2/%{name}.conf
%{_unitdir}/ksm.service
%{_libexecdir}/ksmctl
%config(noreplace) %{_sysconfdir}/sysconfig/ksm
%{_unitdir}/ksmtuned.service
%{_sbindir}/ksmtuned
%{_udevdir}/udev-kvm-check
%{_udevrulesdir}/81-kvm-rhel.rules
%ghost %{_sysconfdir}/kvm
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/bridge.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/vhost.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%{_datadir}/%{name}/simpletrace.py*
%{_datadir}/%{name}/tracetool/*.py*
%{_datadir}/%{name}/tracetool/backend/*.py*
%{_datadir}/%{name}/tracetool/format/*.py*

%files -n qemu-kvm-core
%defattr(-,root,root)
%ifarch x86_64
    %{_datadir}/%{name}/bios.bin
    %{_datadir}/%{name}/bios-256k.bin
    %{_datadir}/%{name}/linuxboot.bin
    %{_datadir}/%{name}/multiboot.bin
    %{_datadir}/%{name}/kvmvapic.bin
    %{_datadir}/%{name}/sgabios.bin
%endif
%ifarch s390x
    %{_datadir}/%{name}/s390-ccw.img
    %{_datadir}/%{name}/s390-netboot.img
%endif
%ifnarch aarch64 s390x
    %{_datadir}/%{name}/vgabios.bin
    %{_datadir}/%{name}/vgabios-cirrus.bin
    %{_datadir}/%{name}/vgabios-qxl.bin
    %{_datadir}/%{name}/vgabios-stdvga.bin
    %{_datadir}/%{name}/vgabios-vmware.bin
    %{_datadir}/%{name}/vgabios-virtio.bin
    %{_datadir}/%{name}/vgabios-ramfb.bin
    %{_datadir}/%{name}/vgabios-bochs-display.bin
    %{_datadir}/%{name}/vgabios-ati.bin
    %{_datadir}/%{name}/efi-e1000.rom
    %{_datadir}/%{name}/efi-e1000e.rom
    %{_datadir}/%{name}/efi-eepro100.rom
    %{_datadir}/%{name}/efi-ne2k_pci.rom
    %{_datadir}/%{name}/efi-pcnet.rom
    %{_datadir}/%{name}/efi-rtl8139.rom
    %{_datadir}/%{name}/efi-virtio.rom
    %{_datadir}/%{name}/efi-vmxnet3.rom
%endif
%{_datadir}/%{name}/qemu-icon.bmp
%{_datadir}/%{name}/qemu_logo_no_text.svg
%{_datadir}/%{name}/linuxboot_dma.bin
%{_datadir}/%{name}/dump-guest-memory.py*
%ifarch %{power64}
    %{_datadir}/%{name}/spapr-rtas.bin
%endif
%{?qemu_kvm_files:}
%if 0%{have_kvm_setup}
    %{_prefix}/lib/systemd/kvm-setup
    %{_unitdir}/kvm-setup.service
    %{_presetdir}/85-kvm.preset
%endif
%if 0%{have_memlock_limits}
    %{_sysconfdir}/security/limits.d/95-kvm-memlock.conf
%endif

%files -n qemu-img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*

%files -n qemu-guest-agent
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevrulesdir}/99-qemu-guest-agent.rules
%config(noreplace) %{_sysconfdir}/sysconfig/qemu-ga
%{_sysconfdir}/qemu-ga
%{_datadir}/%{name}/qemu-ga
%dir %{_localstatedir}/log/qemu-ga

%files tests
%{testsdir}

%files block-curl
%{_libdir}/qemu-kvm/block-curl.so

%if %{have_gluster}
%files block-gluster
%{_libdir}/qemu-kvm/block-gluster.so
%endif

%files block-iscsi
%{_libdir}/qemu-kvm/block-iscsi.so

%files block-rbd
%{_libdir}/qemu-kvm/block-rbd.so

%files block-ssh
%{_libdir}/qemu-kvm/block-ssh.so


%changelog
* Mon Mar 05 2018 Danilo de Paula <ddepaula@redhat.com> - 2.11.0-5.el8
- Prepare building on RHEL-8.0
