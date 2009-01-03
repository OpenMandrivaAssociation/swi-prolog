# Package contains plugins not built by libtool: must disable
# underlinking prevention - AdamW 2008/06
%define _disable_ld_no_undefined 1

%define _requires_exceptions /usr/bin/../pl.sh

Summary:	Prolog interpreter and compiler
Name:		swi-prolog
Version:	5.6.63
Release:	%mkrel 1
License:	LGPLv2+
Group:		Development/Other
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	jpeg-devel
BuildRequires:	xpm-devel
BuildRequires:	X11-devel
BuildRequires:	unixODBC-devel
BuildRequires:	db4-devel
BuildRequires:	openssl-devel
BuildRequires:	libncursesw-devel
BuildRequires:	gmp-devel
BuildRequires:	java-rpmbuild
URL:		http://www.swi-prolog.org/
Source0:	ftp://swi.psy.uva.nl/pub/SWI-Prolog/pl-%{version}.tar.gz
Patch0:		pl-5.6.63-format-string.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes:	swi-pl
Provides:	swi-pl

%description
Edinburgh-style Prolog compiler including modules, autoload, libraries,
Garbage-collector, stack-expandor, C-interface, GNU-readline and GNU-Emacs
interface, very fast compiler.

%package jpl
Group:		Development/Java
Summary:	Java interface for %{name}
Requires:	java >= 1.6.0
Requires:	%{name} = %{version}-%{release}

%description jpl
JPL is a dynamic, bi-directional interface between %{name} and Java
runtimes. It offers two APIs: Java API (Java-calls-Prolog) and Prolog
API (Prolog-calls-Java).

%package xpce
Group:		Development/Other
Summary:	%{name} native GUI library
Requires:	%{name} = %{version}-%{release}

%description xpce
XPCE is a toolkit for developing graphical applications in Prolog and
other interactive and dynamically typed languages. 

%prep
%setup -n pl-%{version} -q
%patch0 -p1 -b .format-string

%build
%{?__cputoolize: %{__cputoolize} -c src} 
%configure2_5x --with-world
make COFLAGS="%{optflags} -fno-strict-aliasing -fPIC"
#make check
pushd packages
export PATH=$PATH:%{_builddir}/pl-%{version}/src
%configure2_5x
make COFLAGS="%{optflags} -fno-strict-aliasing -fPIC" LD_LIBRARY_PATH=%{_builddir}/pl-%{version}/lib/%{_arch}-linux/
 
popd

%install
rm -rf %{buildroot}
%makeinstall_std
pushd packages
%makeinstall PLBASE=%{buildroot}%{_libdir}/pl-%{version} LD_LIBRARY_PATH=%{_builddir}/pl-%{version}/lib/%{_arch}-linux/
make html-install PLBASE=%{buildroot}%{_libdir}/pl-%{version}
popd

rm -f %{buildroot}%{_mandir}/man3/readline*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc LSM PORTING README VERSION
%{_bindir}/pl*
%{_libdir}/pl-*
%{_mandir}/*/pl*
%{_libdir}/pkgconfig/pl.pc
%exclude %{_libdir}/pl-%{version}/doc/packages/examples/jpl
%exclude %{_libdir}/pl-%{version}/doc/packages/jpl
%exclude %{_libdir}/pl-%{version}/lib/*/libjpl.so
%exclude %{_libdir}/pl-%{version}/lib/jpl.jar
%exclude %{_libdir}/pl-%{version}/library/jpl.pl
%exclude %{_libdir}/pl-%{version}/doc/Manual/*xpce.html
%exclude %{_libdir}/pl-%{version}/xpce*


%files jpl
%defattr(-,root,root,0755)
%doc packages/jpl/README.html
%{_libdir}/pl-%{version}/doc/packages/examples/jpl
%{_libdir}/pl-%{version}/doc/packages/jpl
%{_libdir}/pl-%{version}/lib/*/libjpl.so
%{_libdir}/pl-%{version}/lib/jpl.jar
%{_libdir}/pl-%{version}/library/jpl.pl

%files xpce
%defattr(-,root,root,0755)
%{_mandir}/*/xpce*
%{_bindir}/xpce*
%{_libdir}/pl-%{version}/doc/Manual/*xpce.html
%{_libdir}/pl-%{version}/xpce*

