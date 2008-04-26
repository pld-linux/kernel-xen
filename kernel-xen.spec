#
# TODO:
# - port grsec_minimal
# - legal stuff ( http://www.xensource.com/Pages/legal.aspx )
#
# Status:
# - dom0 boots
# - domU doesn't
#
# Conditional build:
%bcond_without	source		# don't build kernel-source package
%bcond_with	verbose		# verbose build (V=1)
#

%{?debug:%define with_verbose 1}

%ifarch %{ix86}
	%define		have_isa	1
%else
	%define		have_isa	0
%endif

%define		have_pcmcia	1
%define		have_oss	1
%define		have_sound	1

%define		xen_version		3.2.0

%define		alt_kernel	xen

%define		_basever	2.6.18
%define		_postver	.8
%define		_rel		0.6
%define		_ver		%{nil}

Summary:	The Linux kernel (the core of the Linux operating system)
Summary(de.UTF-8):	Der Linux-Kernel (Kern des Linux-Betriebssystems)
Summary(et.UTF-8):	Linuxi kernel (ehk operatsioonisüsteemi tuum)
Summary(fr.UTF-8):	Le Kernel-Linux (La partie centrale du systeme)
Summary(pl.UTF-8):	Jądro Linuksa
Name:		kernel-%{alt_kernel}
Version:	%{?_ver:%{_ver}}%{_basever}%{_postver}
Release:	%{?_rc:%{_rc}}%{_rel}
Epoch:		3
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{_basever}.tar.bz2
# Source0-md5:	296a6d150d260144639c3664d127d174
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{_basever}%{_postver}.bz2
# Source1-md5:	090f582d2a0e1951d500b2e55f7df7b4
Source2:	kernel-xen-module-build.pl
Source3:	kernel-xen-config.h
Source20:	kernel-xen-common.config
Source21:	kernel-xen-i386.config
Source22:	kernel-xen-x86_64.config
Source23:	kernel-xen-netfilter.config
Source24:	kernel-xen-xen.config
# from xen-unstable.hg
Patch0:		kernel-xen-xen.patch
URL:		http://www.kernel.org/
BuildRequires:	binutils >= 3:2.14.90.0.7
BuildRequires:	gcc >= 5:3.2
BuildRequires:	module-init-tools
# for hostname command
BuildRequires:	net-tools
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	sed >= 4.0
Autoreqprov:	no
Requires:	/sbin/depmod
Requires:	coreutils
Requires:	geninitrd >= 2.57
Requires:	module-init-tools >= 0.9.9
Provides:	%{name}(vermagic) = %{kernel_release}
Provides:	kernel(xen0) = %{xen_version}
Conflicts:	e2fsprogs < 1.29
Conflicts:	isdn4k-utils < 3.1pre1
Conflicts:	jfsutils < 1.1.3
Conflicts:	module-init-tools < 0.9.10
Conflicts:	nfs-utils < 1.0.5
Conflicts:	oprofile < 0.9
Conflicts:	ppp < 1:2.4.0
Conflicts:	procps < 3.2.0
Conflicts:	quota-tools < 3.09
Conflicts:	reiserfsprogs < 3.6.3
Conflicts:	udev < 1:071
Conflicts:	util-linux < 2.10o
Conflicts:	xfsprogs < 2.6.0
ExclusiveArch:	%{ix86} %{x8664}
ExcludeArch:	i386 i486 i586
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# No ELF objects there to strip (skips processing 27k files)
%define		_noautostrip	.*%{_kernelsrcdir}/.*
%define		_noautochrpath	.*%{_kernelsrcdir}/.*

%define		initrd_dir	/boot

# kernel release (used in filesystem and eventually in uname -r)
# modules will be looked from /lib/modules/%{kernel_release}%{?smp}
# _localversion is just that without version for "> localversion"
%define		_localversion %{release}
%define		kernel_release %{version}_%{alt_kernel}-%{_localversion}
%define		_kernelsrcdir	/usr/src/linux-%{version}_%{alt_kernel}

%define	CommonOpts	HOSTCC="%{__cc}" HOSTCFLAGS="-Wall -Wstrict-prototypes %{rpmcflags} -fomit-frame-pointer" AWK="gawk"
%if "%{_target_base_arch}" != "%{_arch}"
	%define	MakeOpts %{CommonOpts} ARCH=%{_target_base_arch} CROSS_COMPILE=%{_target_cpu}-pld-linux-
	%define	DepMod /bin/true

	%if "%{_arch}" == "x86_64" && "%{_target_base_arch}" == "i386"
	%define	MakeOpts %{CommonOpts} CC="%{__cc}" ARCH=%{_target_base_arch}
	%define	DepMod /sbin/depmod
	%endif

%else
	%define MakeOpts %{CommonOpts} CC="%{__cc}"
	%define	DepMod /sbin/depmod
%endif

%description
This package contains the Linux kernel that is used to boot and run
your system. It contains few device drivers for specific hardware.
Most hardware is instead supported by modules loaded after booting.

%description -l de.UTF-8
Das Kernel-Packet enthält den Linux-Kernel (vmlinuz), den Kern des
Linux-Betriebssystems. Der Kernel ist für grundliegende
Systemfunktionen verantwortlich: Speicherreservierung,
Prozeß-Management, Geräte Ein- und Ausgaben, usw.

%description -l fr.UTF-8
Le package kernel contient le kernel linux (vmlinuz), la partie
centrale d'un système d'exploitation Linux. Le noyau traite les
fonctions basiques d'un système d'exploitation: allocation mémoire,
allocation de process, entrée/sortie de peripheriques, etc.

%description -l pl.UTF-8
Pakiet zawiera jądro Linuksa niezbędne do prawidłowego działania
Twojego komputera. Zawiera w sobie sterowniki do sprzętu znajdującego
się w komputerze, takiego jak sterowniki dysków itp.

%package vmlinux
Summary:	vmlinux - uncompressed kernel image
Summary(de.UTF-8):	vmlinux - dekompressiertes Kernel Bild
Summary(pl.UTF-8):	vmlinux - rozpakowany obraz jądra
Group:		Base/Kernel

%description vmlinux
vmlinux - uncompressed kernel image.

%description vmlinux -l de.UTF-8
vmlinux - dekompressiertes Kernel Bild.

%description vmlinux -l pl.UTF-8
vmlinux - rozpakowany obraz jądra.

%package drm
Summary:	DRM kernel modules
Summary(de.UTF-8):	DRM Kernel Treiber
Summary(pl.UTF-8):	Sterowniki DRM
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description drm
DRM kernel modules.

%description drm -l de.UTF-8
DRM Kernel Treiber.

%description drm -l pl.UTF-8
Sterowniki DRM.

%package pcmcia
Summary:	PCMCIA modules
Summary(de.UTF-8):	PCMCIA Module
Summary(pl.UTF-8):	Moduły PCMCIA
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Conflicts:	pcmcia-cs < 3.1.21
Conflicts:	pcmciautils < 004
Autoreqprov:	no

%description pcmcia
PCMCIA modules.

%description pcmcia -l de.UTF-8
PCMCIA Module.

%description pcmcia -l pl.UTF-8
Moduły PCMCIA.

%package sound-alsa
Summary:	ALSA kernel modules
Summary(de.UTF-8):	ALSA Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku ALSA
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-alsa
ALSA (Advanced Linux Sound Architecture) sound drivers.

%description sound-alsa -l de.UTF-8
ALSA (Advanced Linux Sound Architecture) Sound-Treiber.

%description sound-alsa -l pl.UTF-8
Sterowniki dźwięku ALSA (Advanced Linux Sound Architecture).

%package sound-oss
Summary:	OSS kernel modules
Summary(de.UTF-8):	OSS Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku OSS
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-oss
OSS (Open Sound System) drivers.

%description sound-oss -l de.UTF-8
OSS (Open Sound System) Treiber.

%description sound-oss -l pl.UTF-8
Sterowniki dźwięku OSS (Open Sound System).

%package headers
Summary:	Header files for the Linux kernel
Summary(de.UTF-8):	Header Dateien für den Linux-Kernel
Summary(pl.UTF-8):	Pliki nagłówkowe jądra Linuksa
Group:		Development/Building
Autoreqprov:	no

%description headers
These are the C header files for the Linux kernel, which define
structures and constants that are needed when rebuilding the kernel or
building kernel modules.

%description headers -l de.UTF-8
Dies sind die C Header Dateien für den Linux-Kernel, die definierte
Strukturen und Konstante beinhalten, die beim rekompilieren des Kernels
oder bei Kernel Modul kompilationen gebraucht werden.

%description headers -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe jądra, niezbędne do rekompilacji jądra
oraz budowania modułów jądra.

%package module-build
Summary:	Development files for building kernel modules
Summary(de.UTF-8):	Development Dateien die beim Kernel Modul kompilationen gebraucht werden
Summary(pl.UTF-8):	Pliki służące do budowania modułów jądra
Group:		Development/Building
Requires:	%{name}-headers = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description module-build
Development files from kernel source tree needed to build Linux kernel
modules from external packages.

%description module-build -l de.UTF-8
Development Dateien des Linux-Kernels die beim kompilieren externer
Kernel Module gebraucht werden.

%description module-build -l pl.UTF-8
Pliki ze drzewa źródeł jądra potrzebne do budowania modułów jądra
Linuksa z zewnętrznych pakietów.

%package source
Summary:	Kernel source tree
Summary(de.UTF-8):	Der Kernel Quelltext
Summary(pl.UTF-8):	Kod źródłowy jądra Linuksa
Group:		Development/Building
Requires:	%{name}-module-build = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description source
This is the source code for the Linux kernel. You can build a custom
kernel that is better tuned to your particular hardware.

%description source -l de.UTF-8
Das Kernel-Source-Packet enthält den source code (C/Assembler-Code)
des Linux-Kernels. Die Source-Dateien werden gebraucht, um viele
C-Programme zu kompilieren, da sie auf Konstanten zurückgreifen, die
im Kernel-Source definiert sind. Die Source-Dateien können auch
benutzt werden, um einen Kernel zu kompilieren, der besser auf Ihre
Hardware ausgerichtet ist.

%description source -l fr.UTF-8
Le package pour le kernel-source contient le code source pour le noyau
linux. Ces sources sont nécessaires pour compiler la plupart des
programmes C, car il dépend de constantes définies dans le code
source. Les sources peuvent être aussi utilisée pour compiler un noyau
personnalisé pour avoir de meilleures performances sur des matériels
particuliers.

%description source -l pl.UTF-8
Pakiet zawiera kod źródłowy jądra systemu.

%package doc
Summary:	Kernel documentation
Summary(de.UTF-8):	Kernel Dokumentation
Summary(pl.UTF-8):	Dokumentacja do jądra Linuksa
Group:		Documentation
Autoreqprov:	no

%description doc
This is the documentation for the Linux kernel, as found in
/usr/src/linux/Documentation directory.

%description doc -l de.UTF-8
Dies ist die Kernel Dokumentation wie sie im 'Documentation'
Verzeichniss vorgefunden werden kann.

%description doc -l pl.UTF-8
Pakiet zawiera dokumentację do jądra Linuksa pochodzącą z katalogu
/usr/src/linux/Documentation.

%prep
%setup -q -n linux-%{_basever}

%if "%{_postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | %{__patch} -p1 -s
%endif
%if "%{_ver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE10} | %{__patch} -p1 -s
%endif

# Fix EXTRAVERSION in main Makefile
sed -i 's#EXTRAVERSION =.*#EXTRAVERSION = %{_postver}_%{alt_kernel}#g' Makefile

sed -i -e '/select INPUT/d' net/bluetooth/hidp/Kconfig

# remove unwanted files after patching (if any)
find . '(' -name '*~' -o -name '*.orig' -o -name '.gitignore' ')' -print0 | xargs -0 -r -l512 rm -f

%patch0 -p1

%build
TuneUpConfigForIX86 () {
%ifarch %{ix86}
	%ifnarch i386
		sed -i 's:CONFIG_M386=y:# CONFIG_M386 is not set:' $1
	%endif
	%ifarch i686
		sed -i 's:# CONFIG_M686 is not set:CONFIG_M686=y:' $1
	%endif
	%ifarch pentium3
		sed -i 's:# CONFIG_MPENTIUMIII is not set:CONFIG_MPENTIUMIII=y:' $1
	%endif
	%ifarch pentium4
		sed -i 's:# CONFIG_MPENTIUM4 is not set:CONFIG_MPENTIUM4=y:' $1
	%endif
	%ifarch athlon
		sed -i 's:# CONFIG_MK7 is not set:CONFIG_MK7=y:' $1
	%endif
	%ifarch i686 athlon pentium3 pentium4
		sed -i "s:CONFIG_HIGHMEM4G=y:# CONFIG_HIGHMEM4G is not set:" $1
		sed -i "s:# CONFIG_HIGHMEM64G is not set:CONFIG_HIGHMEM64G=y\nCONFIG_X86_PAE=y:" $1
		sed -i 's:CONFIG_MATH_EMULATION=y:# CONFIG_MATH_EMULATION is not set:' $1
	%endif
	return 0
%endif
}

rm -f .config
BuildConfig() {
	%{?debug:set -x}
	Config="%{_target_base_arch}"
	KernelVer=%{kernel_release}

	echo "Building config file [using $Config.conf] ..."

	# start with an empty config
	echo "" > .config

	# common opts
	cat %{SOURCE20} > .config

	# arch-specific
	cat $RPM_SOURCE_DIR/kernel-xen-$Config.config >> .config

	# fix localversion
	echo "CONFIG_LOCALVERSION=\"-%{_localversion}\"" >> .config

	TuneUpConfigForIX86 .config

	# netfilter
	cat %{SOURCE23} >> .config

	# xen
	cat %{SOURCE24} >> .config

	%{?debug:sed -i "s:# CONFIG_DEBUG_SLAB is not set:CONFIG_DEBUG_SLAB=y:" .config}
	%{?debug:sed -i "s:# CONFIG_DEBUG_PREEMPT is not set:CONFIG_DEBUG_PREEMPT=y:" .config}
	%{?debug:sed -i "s:# CONFIG_RT_DEADLOCK_DETECT is not set:CONFIG_RT_DEADLOCK_DETECT=y:" .config}

	install .config arch/%{_target_base_arch}/defconfig
	install -d $KERNEL_INSTALL_DIR%{_kernelsrcdir}/include/linux
	rm -f include/linux/autoconf.h
	%{__make} %{MakeOpts} include/linux/autoconf.h
	install include/linux/autoconf.h \
		$KERNEL_INSTALL_DIR%{_kernelsrcdir}/include/linux/autoconf-dist.h
	install .config \
		$KERNEL_INSTALL_DIR%{_kernelsrcdir}/config-dist
	install .config arch/%{_target_base_arch}/defconfig
}

BuildKernel() {
	%{?debug:set -x}
	echo "Building kernel $1 ..."
	%{__make} %{MakeOpts} mrproper \
		RCS_FIND_IGNORE='-name build-done -prune -o'
	install arch/%{_target_base_arch}/defconfig .config

	%{__make} %{MakeOpts} clean \
		RCS_FIND_IGNORE='-name build-done -prune -o'

	%{__make} %{MakeOpts} include/linux/version.h \
		%{?with_verbose:V=1}
	%{__make} %{MakeOpts} \
		%{?with_verbose:V=1}
}

PreInstallKernel() {
	Config="%{_target_base_arch}"
	KernelVer=%{kernel_release}

	mkdir -p $KERNEL_INSTALL_DIR/boot
	install System.map $KERNEL_INSTALL_DIR/boot/System.map-$KernelVer
	install arch/%{_target_base_arch}/boot/vmlinuz $KERNEL_INSTALL_DIR/boot/vmlinuz-$KernelVer
	install vmlinux $KERNEL_INSTALL_DIR/boot/vmlinux-$KernelVer

	%{__make} %{MakeOpts} modules_install \
		%{?with_verbose:V=1} \
		DEPMOD=%{DepMod} \
		INSTALL_MOD_PATH=$KERNEL_INSTALL_DIR \
		KERNELRELEASE=$KernelVer

	install Module.symvers \
		$KERNEL_INSTALL_DIR%{_kernelsrcdir}/Module.symvers-dist

	echo "CHECKING DEPENDENCIES FOR KERNEL MODULES"
	%if "%{_target_base_arch}" != "%{_arch}"
		touch $KERNEL_INSTALL_DIR/lib/modules/$KernelVer/modules.dep
	%else
		/sbin/depmod --basedir $KERNEL_INSTALL_DIR -ae \
			-F $KERNEL_INSTALL_DIR/boot/System.map-$KernelVer -r $KernelVer \
			|| echo
	%endif
	echo "KERNEL RELEASE $KernelVer DONE"
}

KERNEL_BUILD_DIR=`pwd`

# SMP KERNEL
KERNEL_INSTALL_DIR="$KERNEL_BUILD_DIR/build-done/kernel"
rm -rf $KERNEL_INSTALL_DIR
BuildConfig
#exit 0
BuildKernel
PreInstallKernel

%install
rm -rf $RPM_BUILD_ROOT
umask 022
export DEPMOD=%{DepMod}

install -d $RPM_BUILD_ROOT%{_kernelsrcdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{kernel_release}

# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al COPYING $RPM_BUILD_ROOT/COPYING 2>/dev/null; then
	l=l
	rm -f $RPM_BUILD_ROOT/COPYING
fi

KERNEL_BUILD_DIR=`pwd`

cp -a$l $KERNEL_BUILD_DIR/build-done/kernel/* $RPM_BUILD_ROOT

	if [ -e  $RPM_BUILD_ROOT/lib/modules/%{kernel_release}$i ] ; then
		rm -f $RPM_BUILD_ROOT/lib/modules/%{kernel_release}$i/build
		ln -sf %{_kernelsrcdir} \
			$RPM_BUILD_ROOT/lib/modules/%{kernel_release}$i/build
		install -d $RPM_BUILD_ROOT/lib/modules/%{kernel_release}$i/{cluster,misc}
	fi

find . -maxdepth 1 ! -name "build-done" ! -name "." -exec cp -a$l "{}" "$RPM_BUILD_ROOT%{_kernelsrcdir}/" ";"

cd $RPM_BUILD_ROOT%{_kernelsrcdir}

%{__make} %{MakeOpts} mrproper \
	RCS_FIND_IGNORE='-name build-done -prune -o'

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

if [ -e $KERNEL_BUILD_DIR/build-done/kernel%{_kernelsrcdir}/include/linux/autoconf-dist.h ]; then
	install $KERNEL_BUILD_DIR/build-done/kernel%{_kernelsrcdir}/include/linux/autoconf-dist.h \
		$RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux
	install	$KERNEL_BUILD_DIR/build-done/kernel%{_kernelsrcdir}/config-dist \
		$RPM_BUILD_ROOT%{_kernelsrcdir}
fi

install $KERNEL_BUILD_DIR/build-done/kernel%{_kernelsrcdir}/include/linux/* \
	$RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux

install $KERNEL_BUILD_DIR/build-done/kernel%{_kernelsrcdir}/config-dist \
	.config
%{__make} %{MakeOpts} include/linux/version.h include/linux/utsrelease.h
mv include/linux/version.h{,.save}
mv include/linux/utsrelease.h{,.save}
%{__make} %{MakeOpts} mrproper
mv include/linux/version.h{.save,}
mv include/linux/utsrelease.h{.save,}
#install %{SOURCE3} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/autoconf.h
install %{SOURCE3} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/config.h

# collect module-build files and directories
%{__perl} %{SOURCE2} %{_kernelsrcdir} $KERNEL_BUILD_DIR

# ghosted initrd
touch $RPM_BUILD_ROOT/boot/initrd-%{kernel_release}.gz

%clean
rm -rf $RPM_BUILD_ROOT

%preun
rm -f /lib/modules/%{kernel_release}/modules.*
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --remove %{kernel_release}
fi

%post
ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz-%{alt_kernel}
ln -sf System.map-%{kernel_release} /boot/System.map-%{alt_kernel}
if [ ! -e /boot/vmlinuz ]; then
	ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz
	ln -sf System.map-%{alt_kernel} /boot/System.map
	ln -sf initrd-%{alt_kernel} %{initrd_dir}/initrd
fi

%depmod %{kernel_release}

/sbin/geninitrd -f --initrdfs=rom %{initrd_dir}/initrd-%{kernel_release}.gz %{kernel_release}
ln -sf initrd-%{kernel_release}.gz %{initrd_dir}/initrd-%{alt_kernel}

if [ -x /sbin/new-kernel-pkg ]; then
	if [ -f /etc/pld-release ]; then
		title=$(sed 's/^[0-9.]\+ //' < /etc/pld-release)
	else
		title='PLD Linux'
	fi

	title="$title %{alt_kernel}"

	/sbin/new-kernel-pkg --initrdfile=%{initrd_dir}/initrd-%{kernel_release}.gz --install %{kernel_release} --banner "$title"
elif [ -x /sbin/rc-boot ]; then
	/sbin/rc-boot 1>&2 || :
fi

%post vmlinux
ln -sf vmlinux-%{kernel_release} /boot/vmlinux-%{alt_kernel}

%post drm
%depmod %{kernel_release}

%postun drm
%depmod %{kernel_release}

%post pcmcia
%depmod %{kernel_release}

%postun pcmcia
%depmod %{kernel_release}

%post sound-alsa
%depmod %{kernel_release}

%postun sound-alsa
%depmod %{kernel_release}

%post sound-oss
%depmod %{kernel_release}

%postun sound-oss
%depmod %{kernel_release}

%post headers
rm -f %{_prefix}/src/linux-%{alt_kernel}
ln -snf %{basename:%{_kernelsrcdir}} %{_prefix}/src/linux-%{alt_kernel}

%postun headers
if [ "$1" = "0" ]; then
	if [ -L %{_prefix}/src/linux-%{alt_kernel} ]; then
		if [ "$(readlink %{_prefix}/src/linux-%{alt_kernel})" = "linux-%{version}_%{alt_kernel}" ]; then
			rm -f %{_prefix}/src/linux-%{alt_kernel}
		fi
	fi
fi

%files
%defattr(644,root,root,755)
/boot/vmlinuz-%{kernel_release}
/boot/System.map-%{kernel_release}
%ghost /boot/initrd-%{kernel_release}.gz
%dir /lib/modules/%{kernel_release}
%dir /lib/modules/%{kernel_release}/kernel
/lib/modules/%{kernel_release}/kernel/arch
/lib/modules/%{kernel_release}/kernel/crypto
/lib/modules/%{kernel_release}/kernel/drivers
#%if %{have_oss} && %{have_isa}
#%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/radio/miropcm20*.ko*
#%endif
/lib/modules/%{kernel_release}/kernel/fs
/lib/modules/%{kernel_release}/kernel/kernel
/lib/modules/%{kernel_release}/kernel/lib
/lib/modules/%{kernel_release}/kernel/net
/lib/modules/%{kernel_release}/kernel/security
%dir /lib/modules/%{kernel_release}/kernel/sound
/lib/modules/%{kernel_release}/kernel/sound/soundcore.*
%dir /lib/modules/%{kernel_release}/misc
%if %{have_pcmcia}
%exclude /lib/modules/%{kernel_release}/kernel/drivers/pcmcia
%exclude /lib/modules/%{kernel_release}/kernel/drivers/*/pcmcia
%exclude /lib/modules/%{kernel_release}/kernel/drivers/bluetooth/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/ide/legacy/ide-cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/parport/parport_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/serial/serial_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/telephony/ixj_pcmcia.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/usb/host/sl811_cs.ko*
%endif
%ghost /lib/modules/%{kernel_release}/modules.*
%dir %{_sysconfdir}/modprobe.d/%{kernel_release}

%files vmlinux
%defattr(644,root,root,755)
/boot/vmlinux-%{kernel_release}

%if %{have_pcmcia}
%files pcmcia
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/drivers/pcmcia
/lib/modules/%{kernel_release}/kernel/drivers/*/pcmcia
/lib/modules/%{kernel_release}/kernel/drivers/bluetooth/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/ide/legacy/ide-cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/parport/parport_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/serial/serial_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/telephony/ixj_pcmcia.ko*
/lib/modules/%{kernel_release}/kernel/drivers/usb/host/sl811_cs.ko*
/lib/modules/%{kernel_release}/kernel/sound/pcmcia
%endif

%if %{have_sound}
%files sound-alsa
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/sound
%exclude %dir /lib/modules/%{kernel_release}/kernel/sound
%exclude /lib/modules/%{kernel_release}/kernel/sound/soundcore.*
%if %{have_oss}
%exclude /lib/modules/%{kernel_release}/kernel/sound/oss
%endif
%if %{have_pcmcia}
%exclude /lib/modules/%{kernel_release}/kernel/sound/pcmcia
%endif

%if %{have_oss}
%files sound-oss
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/sound/oss
%endif			# %{have_oss}
%endif			# %{have_sound}

%files headers
%defattr(644,root,root,755)
%dir %{_kernelsrcdir}
%{_kernelsrcdir}/include
%{_kernelsrcdir}/config-dist
%{_kernelsrcdir}/Module.symvers-dist

%files module-build -f aux_files
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/build
%{_kernelsrcdir}/Kbuild
%{_kernelsrcdir}/arch/*/kernel/asm-offsets.*
%{_kernelsrcdir}/arch/*/kernel/sigframe.h
%dir %{_kernelsrcdir}/scripts
%dir %{_kernelsrcdir}/scripts/kconfig
%{_kernelsrcdir}/scripts/Kbuild.include
%{_kernelsrcdir}/scripts/Makefile*
%{_kernelsrcdir}/scripts/basic
%{_kernelsrcdir}/scripts/mkmakefile
%{_kernelsrcdir}/scripts/mod
%{_kernelsrcdir}/scripts/setlocalversion
%{_kernelsrcdir}/scripts/*.c
%{_kernelsrcdir}/scripts/*.sh
%{_kernelsrcdir}/scripts/kconfig/*

%files doc
%defattr(644,root,root,755)
%{_kernelsrcdir}/Documentation

%if %{with source}
%files source -f aux_files_exc
%defattr(644,root,root,755)
%{_kernelsrcdir}/arch/*/[!Mk]*
%{_kernelsrcdir}/arch/*/kernel/[!M]*
%exclude %{_kernelsrcdir}/arch/*/kernel/asm-offsets.*
%exclude %{_kernelsrcdir}/arch/*/kernel/sigframe.h
%{_kernelsrcdir}/block
%{_kernelsrcdir}/crypto
%{_kernelsrcdir}/drivers
%{_kernelsrcdir}/fs
%if %{with grsec_minimal}
%{_kernelsrcdir}/grsecurity
%endif
%{_kernelsrcdir}/init
%{_kernelsrcdir}/ipc
%{_kernelsrcdir}/kernel
%{_kernelsrcdir}/lib
%{_kernelsrcdir}/mm
%{_kernelsrcdir}/net
%{_kernelsrcdir}/scripts/*
%exclude %{_kernelsrcdir}/scripts/Kbuild.include
%exclude %{_kernelsrcdir}/scripts/Makefile*
%exclude %{_kernelsrcdir}/scripts/basic
%exclude %{_kernelsrcdir}/scripts/kconfig
%exclude %{_kernelsrcdir}/scripts/mkmakefile
%exclude %{_kernelsrcdir}/scripts/mod
%exclude %{_kernelsrcdir}/scripts/setlocalversion
%exclude %{_kernelsrcdir}/scripts/*.c
%exclude %{_kernelsrcdir}/scripts/*.sh
%{_kernelsrcdir}/sound
%{_kernelsrcdir}/security
%{_kernelsrcdir}/usr
%{_kernelsrcdir}/COPYING
%{_kernelsrcdir}/CREDITS
%{_kernelsrcdir}/MAINTAINERS
%{_kernelsrcdir}/README
%{_kernelsrcdir}/REPORTING-BUGS
%endif
