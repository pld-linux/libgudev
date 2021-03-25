#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	tests		# tests (with umockdev)
#
Summary:	GObject bindings for libudev
Summary(pl.UTF-8):	Wiązania GObject do libudev
Name:		libgudev
Version:	236
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libgudev/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	ad5a63bd88fe97189fec7b7afb2d4150
Patch0:		%{name}-gtkdoc.patch
URL:		https://wiki.gnome.org/Projects/libgudev
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	gobject-introspection-devel >= 1.31.1
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	meson >= 0.53.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:199
%{?with_tests:BuildRequires:	umockdev-devel}
BuildRequires:	vala >= 2:0.38.0
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

%package -n vala-libgudev
Summary:	Vala API for libgudev library
Summary(pl.UTF-8):	API języka Vala do biblioteki libgudev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.38.0

%description -n vala-libgudev
Vala API for libgudev library.

%description -n vala-libgudev -l pl.UTF-8
API języka Vala do biblioteki libgudev.

%package apidocs
Summary:	libgudev API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libgudev
Group:		Documentation
Requires:	gtk-doc-common
Obsoletes:	udev-glib-apidocs < 1:230
BuildArch:	noarch

%description apidocs
API documentation for libgudev library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libgudev.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true} \
	%{!?with_tests:-Dtests=disabled}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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

%files -n vala-libgudev
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gudev-1.0.deps
%{_datadir}/vala/vapi/gudev-1.0.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gudev
%endif
