Summary:	DBus-C++ Library Public API Calls
Name:		dbus-c++
Version:	0.9.0
Release:	3
License:	LGPL
Group:		Libraries
Source0:	http://downloads.sourceforge.net/project/dbus-cplusplus/dbus-c++/0.9.0/lib%{name}-%{version}.tar.gz
# Source0-md5:	e752116f523fa88ef041e63d3dee4de2
Patch0:		%{name}-undefined_reference.patch
Patch1:		%{name}-gcc47.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	glib-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# should be linked to dbus-c++
%define		skip_post_check_so	'.+(glib).+\.so.+'

%description
DBus-c++ attempts to provide a C++ API for D-BUS. The library has
a glib and an Ecore mainloop integration. It also offers an optional
own main loop.

%package glib
Summary:	DBus-C++ Library Public API Calls - glib integration
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description glib
glib integration for DBus-C++ library.

%package devel
Summary:	Header files for DBus-C++ library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for DBus-C++ library.

%package glib-devel
Summary:	Header files for DBus-C++-glib library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description glib-devel
This is the package containing the header files for DBus-C++-glib
library.

%prep
%setup -qn lib%{name}-%{version}
%patch0 -p1
%patch1 -p0

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static	\
	--enable-ecore=no	\
	--enable-examples=no	\
	--enable-tests=no
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%post	glib -p /usr/sbin/ldconfig
%postun	glib -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %ghost %{_libdir}/libdbus-c++-1.so.?
%attr(755,root,root) %{_libdir}/libdbus-c++-1.so.*.*.*

%files glib
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libdbus-c++-glib-1.so.?
%attr(755,root,root) %{_libdir}/libdbus-c++-glib-1.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libdbus-c++-1.so
%dir %{_includedir}/dbus-c++-1
%dir %{_includedir}/dbus-c++-1/dbus-c++
%{_includedir}/dbus-c++-1/dbus-c++/*.h
%exclude %{_includedir}/dbus-c++-1/dbus-c++/glib-integration.h
%{_pkgconfigdir}/dbus-c++-1.pc

%files glib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-c++-glib-1.so
%{_includedir}/dbus-c++-1/dbus-c++/glib-integration.h
%{_pkgconfigdir}/dbus-c++-glib-1.pc

