#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	nestegg - WebM demuxer library
Summary(pl.UTF-8):	nestegg - biblioteka demuksera WebM
Name:		libnestegg
Version:	0.1
Release:	0.20110325.1
License:	ISC-like
Group:		Libraries
# git clone git://github.com/kinetiknz/nestegg.git nestegg
Source0:	nestegg.tar.xz
# Source0-md5:	198a8a3223784cf8591adbe94b9cfeb3
URL:		https://github.com/kinetiknz/nestegg/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libtool
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
nestegg is a WebM demuxer library.

%description -l pl.UTF-8
nestegg to biblioteka demuksera WebM.

%package devel
Summary:	Header files for nestegg library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki nestegg
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for nestegg library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki nestegg.

%package static
Summary:	Static nestegg library
Summary(pl.UTF-8):	Statyczna biblioteka nestegg
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static nestegg library.

%description static -l pl.UTF-8
Statyczna biblioteka nestegg.

%package apidocs
Summary:	nestegg API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki nestegg
Group:		Documentation

%description apidocs
API and internal documentation for nestegg library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki nestegg.

%prep
%setup -q -n nestegg

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-doc%{!?with_apidocs:=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies and obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnestegg.la
%if %{with apidocs}
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libnestegg
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README TODO
%attr(755,root,root) %{_libdir}/libnestegg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnestegg.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnestegg.so
%{_includedir}/nestegg
%{_pkgconfigdir}/nestegg.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnestegg.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/*
%endif
