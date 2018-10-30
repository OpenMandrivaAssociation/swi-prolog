%define __noautoreq '/usr/bin/../swipl.sh\\|/usr/bin/swipl\\|/usr/bin/pl'
%define __noautoreqfiles %{_bindir}/../swipl.sh %{_bindir}/swipl %{_libdir}/swipl-%{version}/doc

%define _disable_ld_no_undefined 1

Summary:	Prolog interpreter and compiler
Name:		swi-prolog
Version:	7.2.3
Release:	4
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
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	jpeg-devel
BuildRequires:	xpm-devel
BuildRequires:	pkgconfig(x11)
BuildRequires:	libxft-devel
BuildRequires:	libxinerama-devel
BuildRequires:	pkgconfig(xpm)
BuildRequires:	libxt-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	gmp-devel
Recommends:	%{name}-doc
URL:		http://www.swi-prolog.org/
Source0:	http://www.swi-prolog.org/download/stable/src/swipl-%{version}.tar.gz
Source100:	swi-prolog.rpmlintrc
Patch0:		pl-6.6.6-xpce_package-format_string.patch
Patch1:		pl-6.6.6-jpl_package-fix_configure.patch
Patch2:		swi-prolog-6.6.6-clang.patch

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

%package java
Group:		Development/Java
Summary:	Java interface for %{name}
BuildRequires:	java-devel >= 1.6.0
Requires:	%{name}-nox = %{version}-%{release}
Provides:	%{name}-jpl

%description java
JPL is a dynamic, bi-directional interface between %{name} and Java
runtimes. It offers two APIs: Java API (Java-calls-Prolog) and Prolog
API (Prolog-calls-Java).

%package odbc
Group:		Development/Databases
Summary:	ODBC interface for %{name}
BuildRequires:	unixODBC-devel
Requires:	%{name}-nox = %{version}-%{release}

%description odbc
ODBC interface for SWI-Prolog to interact with database systems.

%package doc
Group:		Documentation
Summary:	Documentation for %{name}
Requires:	%{name}-nox = %{version}-%{release}

%description doc
Documentation for SWI-Prolog.

%prep
%setup -n swipl-%{version} -q
%apply_patches

%build
%configure --enable-shared
%make

pushd packages
%configure
%make
popd

%install
%makeinstall_std -j 1

pushd packages
# cb - using macro causes infinite loop
make install DESTDIR=%{buildroot}
%make html-install PLBASE=%{buildroot}%{_libdir}/swipl-%{version}
popd

%files

%files nox
%doc README VERSION
%{_bindir}/swipl*
%{_libdir}/swipl-%{version}
%{_libdir}/pkgconfig/swipl.pc
%exclude %{_libdir}/swipl-%{version}/doc
%exclude %{_libdir}/swipl-%{version}/lib/*/libjpl.so
%exclude %{_libdir}/swipl-%{version}/lib/jpl.jar
%exclude %{_libdir}/swipl-%{version}/library/jpl.pl
%exclude %{_libdir}/swipl-%{version}/xpce/*
%exclude %{_libdir}/swipl-%{version}/lib/*/odbc4pl.so
%exclude %{_libdir}/swipl-%{version}/library/odbc.pl

%files x
%{_mandir}/*/xpce*
%doc %{_libdir}/swipl-%{version}/doc/Manual/*xpce.html
%{_bindir}/xpce*
%{_libdir}/swipl-%{version}/xpce/*

%files java
%doc packages/jpl/README.html
%doc %{_libdir}/swipl-%{version}/doc/packages/examples/jpl
%doc %{_libdir}/swipl-%{version}/doc/packages/jpl
%{_libdir}/swipl-%{version}/lib/*/libjpl.so
%{_libdir}/swipl-%{version}/lib/jpl.jar
%{_libdir}/swipl-%{version}/library/jpl.pl

%files odbc
%doc %{_libdir}/swipl-%{version}/doc/packages/odbc.html
%{_libdir}/swipl-%{version}/lib/*/odbc4pl.so
%{_libdir}/swipl-%{version}/library/odbc.pl

%files doc
%{_mandir}/*/swipl*
%dir %{_libdir}/swipl-%{version}/doc
%doc %{_libdir}/swipl-%{version}/doc/Manual
%exclude %{_libdir}/swipl-%{version}/doc/Manual/*xpce.html
%doc %{_libdir}/swipl-%{version}/doc/packages
%exclude %{_libdir}/swipl-%{version}/doc/packages/examples/jpl
%exclude %{_libdir}/swipl-%{version}/doc/packages/jpl
%exclude %{_libdir}/swipl-%{version}/doc/packages/odbc.html

