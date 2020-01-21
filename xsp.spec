#
# spec file for package xsp
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           xsp
Url:            http://go-mono.com/
Version:	4.7.1
Release:	0.xamarin.1
Summary:        Small Web Server Hosting ASP.NET
License:        MIT
Group:          Productivity/Networking/Web/Servers
Source:         %{name}-%{version}.tar.gz
Source1:        xsp.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  fdupes
BuildRequires:  mono-data-oracle
BuildRequires:  mono-data-sqlite
BuildRequires:  mono-devel
BuildRequires:  mono-web
BuildRequires:  monodoc-core
BuildRequires:  pkgconfig
BuildRequires:  sqlite
%define xspConfigsLocation %{_sysconfdir}/xsp/4.0
%define xspAvailableApps %{xspConfigsLocation}/applications-available
%define xspEnabledApps %{xspConfigsLocation}/applications-enabled

%define debug_package %{nil}

%description
The XSP server is a small Web server that hosts the Mono System.Web
classes for running what is commonly known as ASP.NET.

%prep
%setup -q

%build
#autoreconf -f -i -Wnone
# Cannot use the configure macro because noarch-redhat-linux is not recognized by the auto tools in the tarball
./configure --prefix=%{_prefix} \
	    --libexecdir=%{_prefix}/lib \
	    --libdir=%{_prefix}/lib \
	    --mandir=%{_mandir} \
	    --infodir=%{_infodir} \
	    --sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_prefix}/lib/libfpm_helper.a
rm -f %{buildroot}%{_prefix}/lib/libfpm_helper.la
rm -f %{buildroot}%{_prefix}/lib/libfpm_helper.so
rm -rf %{buildroot}%{_prefix}/lib/xsp/unittests
mkdir -p %{buildroot}%{_datadir}
mv %{buildroot}%{_prefix}/lib/pkgconfig %{buildroot}%{_datadir}
%if 0%{?suse_version}
mkdir -p %{buildroot}/%{xspAvailableApps}
mkdir -p %{buildroot}/%{xspEnabledApps}
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/etc/logrotate.d/
mkdir -p %{buildroot}/srv/xsp4
mkdir -p %{buildroot}/var/adm/fillup-templates
mkdir -p %{buildroot}/run/xsp4
mkdir -p %{buildroot}/usr/lib/tmpfiles.d/
install -m 644 man/mono-asp-apps.1 %{buildroot}%{_mandir}/man1/mono-asp-apps.1
install -m 644 packaging/opensuse/sysconfig.xsp4 %{buildroot}/var/adm/fillup-templates 
install -m 644 packaging/opensuse/xsp4.logrotate %{buildroot}/etc/logrotate.d/xsp4
install -m 755 packaging/opensuse/xsp4.init %{buildroot}/etc/init.d/xsp4
install -m 755 tools/mono-asp-apps/mono-asp-apps %{buildroot}%{_bindir}/mono-asp-apps
install -m 755 %{SOURCE1} %{buildroot}/usr/lib/tmpfiles.d/
%fdupes %{buildroot}
%endif

%clean
rm -rf %{buildroot}

%if 0%{?suse_version}

%post
%{fillup_and_insserv -n xsp4 xsp4}
install -d -m 0711 --owner=wwwrun --group=www /run/xsp4

%preun
%stop_on_removal xsp4

%postun
%restart_on_update xsp4
%{insserv_cleanup}
%endif

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/pkgconfig/*
%{_prefix}/lib/mono/4.5/Mono.WebServer2.dll
%{_prefix}/lib/mono/4.5/fastcgi-mono-server4.exe
%{_prefix}/lib/mono/4.5/mod-mono-server4.exe
%{_prefix}/lib/mono/4.5/xsp4.exe
%{_prefix}/lib/mono/4.5/mono-fpm.exe
%{_prefix}/lib/mono/gac/Mono.WebServer2
%{_prefix}/lib/mono/gac/fastcgi-mono-server4
%{_prefix}/lib/mono/gac/mod-mono-server4
%{_prefix}/lib/mono/gac/mono-fpm
%{_prefix}/lib/mono/gac/xsp4
%{_prefix}/lib/monodoc/sources/Mono.WebServer.*
%{_prefix}/lib/monodoc/sources/Mono.FastCGI.*
%{_prefix}/lib/xsp
%{_prefix}/lib/libfpm_helper.so.0*
%{_prefix}/share/man/*/*
%if 0%{?suse_version}
%config /etc/init.d/xsp4
%config /etc/logrotate.d/xsp4
/var/adm/fillup-templates/*
%attr(0711,wwwrun,www) /srv/xsp4
%ghost %attr(0711,wwwrun,www) /run/xsp4
/usr/lib/tmpfiles.d/
%{_sysconfdir}/%{name}
%endif
%doc NEWS README

%if 0%{?fedora} || 0%{?rhel} || 0%{?centos}
# Allows overrides of __find_provides in fedora distros... (already set to zero on newer suse distros)
%define _use_internal_dependency_generator 0
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/redhat/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort -u'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/redhat/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort -u'
%else
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-provides ; } | sort -u'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | /usr/bin/mono-find-requires ; } | sort -u'
%endif

%changelog

