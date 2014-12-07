%if %{_use_internal_dependency_generator}
%define __noautoreq '/usr/bin/../swipl.sh|/usr/bin/pl'
%else
%define _requires_exceptions /usr/bin/../swipl.sh\\|/usr/bin/pl
%endif

Summary:	Prolog interpreter and compiler
Name:		swi-prolog
Version:	5.10.5
Release:	12
License:	LGPLv2+
Group:		Development/Other
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	readline-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	fontconfig-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	gmp-devel
BuildRequires:	unixODBC-devel
BuildRequires:	java-rpmbuild
URL:		http://www.swi-prolog.org/
Source0:	http://www.swi-prolog.org/download/stable/src/pl-%{version}.tar.gz
Patch0:		pl-5.6.63-format-string.patch
Patch1:		pl-5.10.2-link.patch
Patch2:		pl-5.10.5-32bit_build_fix.diff
Patch3:		pl-5.10.5-CVE-2011-2896.diff
Provides:	swi-pl = %{version}-%{release}

%description
Edinburgh-style Prolog compiler including modules, autoload, libraries,
Garbage-collector, stack-expandor, C-interface, GNU-readline and GNU-Emacs
interface, very fast compiler.

%package jpl
Group:		Development/Java
Summary:	Java interface for %{name}
Requires:	java >= 1.6.0
Requires:	%{name} >= %{version}-%{release}

%description jpl
JPL is a dynamic, bi-directional interface between %{name} and Java
runtimes. It offers two APIs: Java API (Java-calls-Prolog) and Prolog
API (Prolog-calls-Java).

%package xpce
Group:		Development/Other
Summary:	%{name} native GUI library
Requires:	%{name} >= %{version}-%{release}

%description xpce
XPCE is a toolkit for developing graphical applications in Prolog and
other interactive and dynamically typed languages. 

%prep
%setup -n pl-%{version} -q
%patch0 -p1 -b .format-string
%patch1 -p1 -b .link
%patch2 -p1 -b .32bit_build_fix
%patch3 -p0 -b .CVE-2011-2896

%build
%{?__cputoolize: %{__cputoolize} -c src} 
%configure --with-world --enable-shared
%make COFLAGS="%{optflags} -fno-strict-aliasing -fPIC"
#make check
pushd packages
export PATH=$PATH:%{_builddir}/pl-%{version}/src
%configure
%make COFLAGS="%{optflags} -fno-strict-aliasing -fPIC" LD_LIBRARY_PATH=%{_builddir}/pl-%{version}/lib/%{_arch}-linux/
popd

%install
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/lib/%{_target_cpu}-%{_target_os}
%makeinstall_std
pushd packages
%makeinstall PLBASE=%{buildroot}%{_libdir}/swipl-%{version}
%make html-install PLBASE=%{buildroot}%{_libdir}/swipl-%{version}
popd

rm -f %{buildroot}%{_mandir}/man3/readline*

%files
%defattr(-,root,root,0755)
%doc README VERSION
%{_bindir}/swipl*
%{_libdir}/swipl-%{version}
%{_mandir}/*/swipl*
%{_libdir}/pkgconfig/swipl.pc
%exclude %{_libdir}/swipl-%{version}/doc/packages/jpl
%exclude %{_libdir}/swipl-%{version}/lib/*/libjpl.so
%exclude %{_libdir}/swipl-%{version}/lib/jpl.jar
%exclude %{_libdir}/swipl-%{version}/library/jpl.pl
%exclude %{_libdir}/swipl-%{version}/doc/Manual/*xpce.html
%exclude %{_libdir}/swipl-%{version}/xpce*

%files jpl
%defattr(-,root,root,0755)
%doc packages/jpl/README.html
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
