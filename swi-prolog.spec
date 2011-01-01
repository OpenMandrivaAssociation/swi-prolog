%define _requires_exceptions /usr/bin/../swipl.sh\\|/usr/bin/pl

Summary:	Prolog interpreter and compiler
Name:		swi-prolog
Version:	5.10.2
Release:	%mkrel 2
License:	LGPLv2+
Group:		Development/Other
BuildRequires:	ncursesw-devel
BuildRequires:	readline-devel
BuildRequires:	jpeg-devel
BuildRequires:	libxpm-devel
BuildRequires:	libx11-devel
BuildRequires:	libxft-devel
BuildRequires:	libxinerama-devel
BuildRequires:	libxt-devel
Buildrequires:	openssl-devel
BuildRequires:	fontconfig-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	gmp-devel
BuildRequires:	unixODBC-devel
BuildRequires:	java-rpmbuild
URL:		http://www.swi-prolog.org/
Source0:	http://www.swi-prolog.org/download/stable/src/pl-%{version}.tar.gz
Patch0:		pl-5.6.63-format-string.patch
Patch1:		pl-5.10.2-link.patch
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
%patch1 -p0 -b .link

%build
%{?__cputoolize: %{__cputoolize} -c src} 
%configure2_5x --with-world --enable-shared
%make COFLAGS="%{optflags} -fno-strict-aliasing -fPIC"
#make check
pushd packages
export PATH=$PATH:%{_builddir}/pl-%{version}/src
%configure2_5x
%make COFLAGS="%{optflags} -fno-strict-aliasing -fPIC" LD_LIBRARY_PATH=%{_builddir}/pl-%{version}/lib/%{_arch}-linux/ 
popd

%install
rm -rf %{buildroot}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/lib/%{_target_cpu}-%{_target_os}
%makeinstall_std
pushd packages
%makeinstall PLBASE=%{buildroot}%{_libdir}/swipl-%{version}
%make html-install PLBASE=%{buildroot}%{_libdir}/swipl-%{version}
popd

rm -f %{buildroot}%{_mandir}/man3/readline*

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc PORTING README VERSION
%{_bindir}/swipl*
%{_libdir}/swipl-%{version}
%{_mandir}/*/swipl*
%{_libdir}/pkgconfig/swipl.pc
%exclude %{_libdir}/swipl-%{version}/doc/packages/examples/jpl
%exclude %{_libdir}/swipl-%{version}/doc/packages/jpl
%exclude %{_libdir}/swipl-%{version}/lib/*/libjpl.so
%exclude %{_libdir}/swipl-%{version}/lib/jpl.jar
%exclude %{_libdir}/swipl-%{version}/library/jpl.pl
%exclude %{_libdir}/swipl-%{version}/doc/Manual/*xpce.html
%exclude %{_libdir}/swipl-%{version}/xpce*


%files jpl
%defattr(-,root,root,0755)
%doc packages/jpl/README.html
%{_libdir}/swipl-%{version}/doc/packages/examples/jpl
%{_libdir}/swipl-%{version}/doc/packages/jpl
%{_libdir}/swipl-%{version}/lib/*/libjpl.so
%{_libdir}/swipl-%{version}/lib/jpl.jar
%{_libdir}/swipl-%{version}/library/jpl.pl

%files xpce
%defattr(-,root,root,0755)
%{_mandir}/*/xpce*
%{_bindir}/xpce*
%{_libdir}/swipl-%{version}/doc/Manual/*xpce.html
%{_libdir}/swipl-%{version}/xpce*
