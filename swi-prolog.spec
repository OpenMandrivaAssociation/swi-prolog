%define __noautoreq '/usr/bin/../swipl.sh\\|/usr/bin/swipl\\|/usr/bin/pl'
%define __noautoreqfiles %{_bindir}/../swipl.sh %{_bindir}/swipl %{_libdir}/swipl-%{version}/doc

%define _disable_ld_no_undefined 1

Summary:	Prolog interpreter and compiler
Name:		swi-prolog
Version:	8.2.3
Release:	1
License:	LGPLv2+
Group:		Development/Other
Requires:	%{name}-nox
Requires:	%{name}-xpce
Recommends:	%{name}-doc

%description
Edinburgh-style Prolog compiler including modules, autoload, libraries,
Garbage-collector, stack-expandor, C-interface, GNU-readline and GNU-Emacs
interface, very fast compiler.

%package nox
Group:		Development/Other
Summary:	SWI-Prolog without GUI components
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(gmp)
BuildRequires:	jre-current
Recommends:	%{name}-doc
URL:		http://www.swi-prolog.org/
Source0:	http://www.swi-prolog.org/download/stable/src/swipl-%{version}.tar.gz
Source100:	swi-prolog.rpmlintrc
Patch0:		pl-6.6.6-xpce_package-format_string.patch

%description nox
This package provide SWI-Prolog and several libraries, but without
GUI components.

%package x
Group:          Development/Other
Summary:        %{name} native GUI library
Requires:       %{name}-nox = %{version}-%{release}
Provides:	%{name}-xpce

%description x
XPCE is a toolkit for developing graphical applications in Prolog and
other interactive and dynamically typed languages.

%package doc
Group:		Documentation
Summary:	Documentation for %{name}
Requires:	%{name}-nox = %{version}-%{release}

%description doc
Documentation for SWI-Prolog.

%prep
%autosetup -p1 -n swipl-%{version}
export LD_LIBRARY_PATH=`pwd`/build/src:$JAVA_HOME/lib/server
. %{_sysconfdir}/profile.d/90java.sh
%cmake \
	-G Ninja

%build
. %{_sysconfdir}/profile.d/90java.sh
export LD_LIBRARY_PATH=`pwd`/build/src:$JAVA_HOME/lib/server
%ninja_build -C build

%install
. %{_sysconfdir}/profile.d/90java.sh
export LD_LIBRARY_PATH=`pwd`/build/src:$JAVA_HOME/lib/server
%ninja_install -C build

%files

%files nox
%doc VERSION
%{_bindir}/swipl*
%dir %{_prefix}/lib/swipl
%{_prefix}/lib/swipl/boot.prc
%{_prefix}/lib/swipl/*.rc
%{_prefix}/lib/swipl/*.home
%{_prefix}/lib/swipl/*.md
%{_prefix}/lib/swipl/LICENSE
%{_mandir}/man1/swipl.1*
%{_mandir}/man1/swipl-ld.1*
%{_datadir}/pkgconfig/swipl.pc
%{_prefix}/lib/swipl/bin
%{_prefix}/lib/swipl/boot
%{_prefix}/lib/swipl/customize
%{_prefix}/lib/swipl/demo
%{_prefix}/lib/swipl/lib
%{_prefix}/lib/swipl/library
%{_prefix}/lib/swipl/include
%{_prefix}/lib/cmake/swipl

%files x
%{_prefix}/lib/swipl/xpce

%files doc
%{_prefix}/lib/swipl/doc
