Name:           next-server
Version:        0.0.1
Release:        1%{?dist}
Summary:        Next generation proxy server.
Group:          Unspecified
License:        MPL-2.0
URL:            https://github.com/The-NeXT-Project/NeXT-Server
Packager:       The NeXT Project Team <package@nextpanel.dev>
BuildRequires:  systemd

%description
Next generation proxy server.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/next-server
mkdir -p %{buildroot}%{_sysconfdir}/next-server
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/%{name}-%{version}/next-server-amd64-linux %{buildroot}/usr/local/next-server/next-server
install -m 644 %{_builddir}/%{name}-%{version}/geoip.dat %{buildroot}/usr/local/next-server/geoip.dat
install -m 644 %{_builddir}/%{name}-%{version}/geosite.dat %{buildroot}/usr/local/next-server/geosite.dat
install -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}/usr/local/next-server/README.md
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}/usr/local/next-server/LICENSE
install -m 644 %{_builddir}/%{name}-%{version}/dns.json %{buildroot}%{_sysconfdir}/next-server/dns.json
install -m 644 %{_builddir}/%{name}-%{version}/route.json %{buildroot}%{_sysconfdir}/next-server/route.json
install -m 644 %{_builddir}/%{name}-%{version}/custom_outbound.json %{buildroot}%{_sysconfdir}/next-server/custom_outbound.json
install -m 644 %{_builddir}/%{name}-%{version}/custom_inbound.json %{buildroot}%{_sysconfdir}/next-server/custom_inbound.json
install -m 644 %{_builddir}/%{name}-%{version}/rulelist %{buildroot}%{_sysconfdir}/next-server/rulelist
install -m 644 %{_builddir}/%{name}-%{version}/config.yml.example %{buildroot}%{_sysconfdir}/next-server/config.yml.example
install -m 644 %{_builddir}/%{name}-%{version}/next-server.service %{buildroot}%{_sysconfdir}/systemd/system

%post
ln -s /usr/local/next-server/next-server %{_bindir}/next-server

%postun
rm -f %{_bindir}/next-server

%clean
rm -rf %{buildroot}

%files
%attr(0755, root, root) /usr/local/next-server
%attr(0755, root, root) /usr/local/next-server/next-server
%attr(0644, root, root) /usr/local/next-server/geoip.dat
%attr(0644, root, root) /usr/local/next-server/geosite.dat
%attr(0644, root, root) /usr/local/next-server/README.md
%attr(0644, root, root) /usr/local/next-server/LICENSE
%attr(0644, root, root) %{_sysconfdir}/next-server/dns.json
%attr(0644, root, root) %{_sysconfdir}/next-server/route.json
%attr(0644, root, root) %{_sysconfdir}/next-server/custom_outbound.json
%attr(0644, root, root) %{_sysconfdir}/next-server/custom_inbound.json
%attr(0644, root, root) %{_sysconfdir}/next-server/rulelist
%attr(0644, root, root) %{_sysconfdir}/next-server
%attr(0644, root, root) %{_sysconfdir}/next-server/config.yml.example
%attr(0644, root, root) %{_sysconfdir}/systemd/system/next-server.service

%changelog
* Sun Dec 23 2023 The NeXT Project Team <package@nextpanel.dev> - 0.1.0-1
 - https://github.com/The-NeXT-Project/NeXT-Server/releases/tag/v0.1.0
