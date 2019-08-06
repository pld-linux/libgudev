#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	tests		# tests (with umockdev)
#
Summary:	GObject bindings for libudev
Summary(pl.UTF-8):	Wiązania GObject do libudev
Name:		libgudev
Version:	233
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgudev/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	d59a317a40aaa02a2226056c0bb4d3e1
URL:		https://wiki.gnome.org/Projects/libgudev
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	gobject-introspection-devel >= 1.31.1
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:199
%{?with_tests:BuildRequires:	umockdev-devel}
BuildRequires:	xz
Requires:	glib2 >= 1:2.38
Requires:	udev-libs >= 1:199
Provides:	udev-glib = 1:%{version}-%{release}
Obsoletes:	udev-glib < 1:230
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libgudev library provides GObject bindings for libudev.

%description -l pl.UTF-8
Biblioteka libgudev dostarcza wiązania GObject do biblioteki libudev.

%package devel
Summary:	Header files for libgudev library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgudev
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.38
Requires:	udev-devel >= 1:199
Provides:	udev-glib-devel = 1:%{version}-%{release}
Obsoletes:	udev-glib-devel < 1:230

%description devel
Header files for libgudev library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgudev.

%package static
Summary:	Static libgudev library
Summary(pl.UTF-8):	Statyczna biblioteka libgudev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	udev-glib-static = 1:%{version}-%{release}
Obsoletes:	udev-glib-static < 1:230

%description static
Static libgudev library.

%description static -l pl.UTF-8
Statyczna biblioteka libgudev.

%package apidocs
Summary:	libgudev API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libgudev
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	udev-glib-apidocs < 1:230
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libgudev library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libgudev.

%prep
%setup -q

%build
# rebuild ac/am/lt for as-needed to work
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-gtk-doc} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{!?with_tests:--disable-umockdev} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgudev-1.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_libdir}/libgudev-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgudev-1.0.so.0
%{_libdir}/girepository-1.0/GUdev-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgudev-1.0.so
%{_includedir}/gudev-1.0
%{_datadir}/gir-1.0/GUdev-1.0.gir
%{_pkgconfigdir}/gudev-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgudev-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gudev
%endif
