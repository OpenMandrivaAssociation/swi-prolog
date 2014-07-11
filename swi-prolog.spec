%if %{_use_internal_dependency_generator}
%define __noautoreq '/usr/bin/../swipl.sh|/usr/bin/pl'
%else
%define _requires_exceptions /usr/bin/../swipl.sh\\|/usr/bin/pl
%endif

Summary:	Prolog interpreter and compiler
Name:		swi-prolog
Version:	5.10.5
Release:	10
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
Buildrequires:	pkgconfig(openssl)
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
%configure2_5x --with-world --enable-shared
%make COFLAGS="%{optflags} -fno-strict-aliasing -fPIC"
#make check
pushd packages
export PATH=$PATH:%{_builddir}/pl-%{version}/src
%configure2_5x
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


%changelog
* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 5.10.5-3mdv2012.0
+ Revision: 739197
- rebuilt for new unixODBC (second try)

* Thu Dec 08 2011 Oden Eriksson <oeriksson@mandriva.com> 5.10.5-2
+ Revision: 739132
- rebuilt for new unixODBC

* Fri Nov 04 2011 Oden Eriksson <oeriksson@mandriva.com> 5.10.5-1
+ Revision: 717620
- 5.10.5
- rediffed the link fix patch
- P2: fix build on 32bit (pcpa)
- P3: security fix for CVE-2011-2896 (upstream)
- mass rebuild

* Sat Jan 01 2011 Funda Wang <fwang@mandriva.org> 5.10.2-2mdv2011.0
+ Revision: 626986
- bump rel
- fix shared build
- new version 5.10.2

* Sat Jul 31 2010 Ahmad Samir <ahmadsamir@mandriva.org> 5.10.1-2mdv2011.0
+ Revision: 564068
- fix automatic package requires by using _requires_exceptions

* Wed Jul 28 2010 Ahmad Samir <ahmadsamir@mandriva.org> 5.10.1-1mdv2011.0
+ Revision: 562670
- update to 5.10.1
- adapt the name change, pl -> swipl
- drop patch1, not needed and hasn't been applied for some time now
- use %%make, it seems to work OK

* Thu Apr 08 2010 Ahmad Samir <ahmadsamir@mandriva.org> 5.8.3-3mdv2010.1
+ Revision: 533163
- rebuild for openssl-1.0.0

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against openssl-0.9.8m

* Fri Feb 12 2010 Funda Wang <fwang@mandriva.org> 5.8.3-1mdv2010.1
+ Revision: 504742
- new version 5.8.3

* Tue Feb 09 2010 Funda Wang <fwang@mandriva.org> 5.6.64-5mdv2010.1
+ Revision: 502944
- rebuild for new gmp

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 5.6.64-4mdv2010.1
+ Revision: 488804
- rebuilt against libjpeg v8

* Mon Aug 24 2009 Frederik Himpe <fhimpe@mandriva.org> 5.6.64-3mdv2010.0
+ Revision: 420552
- Add patch from Arch Linux to make it build with the new toolchain

  + Oden Eriksson <oeriksson@mandriva.com>
    - deps fixes on wrong package :)
    - fix deps
    - rebuilt against libjpeg v7

* Thu Feb 26 2009 Frederik Himpe <fhimpe@mandriva.org> 5.6.64-1mdv2009.1
+ Revision: 345355
- Update to new version 5.6.64

* Thu Feb 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 5.6.63-2mdv2009.1
+ Revision: 345161
- rebuild against new readline

* Sat Jan 03 2009 Frederik Himpe <fhimpe@mandriva.org> 5.6.63-1mdv2009.1
+ Revision: 323792
- Add patch to fix build with -Werror=format-security
- Install x86_64 modules in /usr/lib64
- Update to new version
- jpl subpackage can work with any Java 1.6.0 environment

  + Adam Williamson <awilliamson@mandriva.org>
    - new release 5.6.56

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 5.6.55-2mdv2009.0
+ Revision: 225544
- rebuild

  + Adam Williamson <awilliamson@mandriva.org>
    - correct the comment (mumblegrumblenitpickinganssigrumblemumble)

* Tue Jun 17 2008 Adam Williamson <awilliamson@mandriva.org> 5.6.55-1mdv2009.0
+ Revision: 221101
- except a bogus automatic require which made package unusable (#40895)
- disable underlinking (package contains plugins not built with libtool)
- new release 5.6.55

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - replaced old buildreq from icedtea to java-rpmbuild

* Mon Mar 03 2008 Adam Williamson <awilliamson@mandriva.org> 5.6.51-1mdv2008.1
+ Revision: 178170
- new release 5.6.51

* Sat Feb 23 2008 Adam Williamson <awilliamson@mandriva.org> 5.6.50-1mdv2008.1
+ Revision: 174100
- build with fPIC (needed on x86-64)
- several new buildrequires for add-ons
- put jpl and xpce in subpackages to reduce deps of main package
- build all the add-ons (much functionality missing without them)
- minor cleanups
- new release 5.6.50

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 07 2007 Adam Williamson <awilliamson@mandriva.org> 5.6.47-2mdv2008.1
+ Revision: 116368
- disable tests; causing odd failure on buildsystem but work fine in manual build
- new license policy
- new release 5.6.47 (requested on forums)


* Tue Sep 26 2006 Pixel <pixel@mandriva.com> 5.4.6-4mdv2007.0
- rebuild for ncurses
- remove old packager tag

* Sun Jan 01 2006 Pixel <pixel@mandrakesoft.com> 5.4.6-3mdk
- Rebuild

* Tue May 03 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 5.4.6-2mdk
- fix lib path
- %%mkrel

* Fri Jan 21 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 5.4.6-1mdk
- 5.4.6
- fix summary-ended-with-dot
- do not remove builddir in %%clean

* Fri Nov 12 2004 Pixel <pixel@mandrakesoft.com> 5.4.3-1mdk
- new release

* Thu Dec 25 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.2.11-1mdk
- 5.2.11

* Tue Oct 21 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.0.10-3mdk
- cputoolize

