%define _sysusersdir %{_prefix}/lib/sysusers.d

Name:          janus
Version:       1.1.0
Release:       1%{?dist}
Summary:       Janus WebRTC Server
License:       GPLv3
URL:           https://janus.conf.meetecho.com/
Source0:       https://github.com/meetecho/janus-gateway/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:       janus.user
Source2:       janus.service
BuildRequires: make
BuildRequires: systemd-rpm-macros
BuildRequires: libmicrohttpd-devel
BuildRequires: jansson-devel
BuildRequires: openssl-devel
BuildRequires: libsrtp-devel
# BuildRequires: sofia-sip-devel # SIP plugin
BuildRequires: glib2-devel
BuildRequires: opus-devel
BuildRequires: libogg-devel
BuildRequires: libcurl-devel
BuildRequires: pkgconfig
BuildRequires: gengetopt
BuildRequires: libconfig-devel
BuildRequires: libnice-devel
BuildRequires: libwebsockets-devel
BuildRequires: librabbitmq-devel
BuildRequires: libpcap-devel
BuildRequires: usrsctp-devel
BuildRequires: npm
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake

%description
Janus is an open source, general purpose, WebRTC server designed and
developed by Meetecho.

%prep
%autosetup -n janus-gateway-%{version} -p1
autoreconf -fiv
%configure
%make_build

%install
%make_install
make configs DESTDIR=%{buildroot}

install -Dm0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/janus.conf
install -Dm0644 %{SOURCE2} %{buildroot}%{_unitdir}/janus.service

rm -f %{buildroot}%{_sysconfdir}/janus/*.sample

%files
%{_bindir}/janus*
%{_libdir}/janus
%{_includedir}/janus
%{_unitdir}/*.service
%{_sysusersdir}/*.conf
%{_datadir}/janus
%{_mandir}/man1/janus*
%{_docdir}/janus-gateway
%config(noreplace) %{_sysconfdir}/janus/*.jcfg

%post
/usr/bin/systemd-sysusers janus.conf
%systemd_post janus.service

%preun
%systemd_preun janus.service

%postun
%systemd_postun_with_restart janus.service

%changelog
