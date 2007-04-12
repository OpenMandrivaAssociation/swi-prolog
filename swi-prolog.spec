%define	name	swi-prolog
%define	version	5.4.6
%define rel	4
%define	release	%mkrel %{rel}

Summary:	Prolog interpreter and compiler
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
BuildRequires:	ncurses-devel readline-devel
URL:		http://www.swi-prolog.org/
Source0:	ftp://swi.psy.uva.nl/pub/SWI-Prolog/pl-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes:	swi-pl
Provides:	swi-pl

%description
Edinburgh-style Prolog compiler including modules, autoload, libraries,
Garbage-collector, stack-expandor, C-interface, GNU-readline and GNU-Emacs
interface, very fast compiler.

%prep
%setup -n pl-%{version} -q

%build
%{?__cputoolize: %{__cputoolize} -c src} 
%configure2_5x
make COFLAGS="%{optflags} -fno-strict-aliasing"
make -C src check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rm -f $RPM_BUILD_ROOT%{_mandir}/man3/readline*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%doc LSM PORTING README VERSION
%{_bindir}/*
%{_prefix}/lib/pl-*
%{_mandir}/*/pl*

