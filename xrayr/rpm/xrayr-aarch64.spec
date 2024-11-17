Name:           xrayr
Version:        0.0.1
Release:        1%{?dist}
Summary:        A Xray backend framework that can easily support many panels.
Group:          Unspecified
License:        MPL-2.0
URL:            https://github.com/XrayR-project/XrayR
Packager:       The NeXT Project Team <package@nextpanel.dev>
BuildRequires:  systemd

%description
A Xray backend framework that can easily support many panels.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/xrayr
mkdir -p %{buildroot}%{_sysconfdir}/xrayr
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/%{name}-%{version}/xrayr-arm64-linux %{buildroot}/usr/local/xrayr/xrayr
install -m 644 %{_builddir}/%{name}-%{version}/dns.json %{buildroot}/usr/local/xrayr/dns.json
install -m 644 %{_builddir}/%{name}-%{version}/route.json %{buildroot}/usr/local/xrayr/route.json
install -m 644 %{_builddir}/%{name}-%{version}/custom_outbound.json %{buildroot}/usr/local/xrayr/custom_outbound.json
install -m 644 %{_builddir}/%{name}-%{version}/custom_inbound.json %{buildroot}/usr/local/xrayr/custom_inbound.json
install -m 644 %{_builddir}/%{name}-%{version}/rulelist %{buildroot}/usr/local/xrayr/rulelist
install -m 644 %{_builddir}/%{name}-%{version}/geoip.dat %{buildroot}/usr/local/xrayr/geoip.dat
install -m 644 %{_builddir}/%{name}-%{version}/geosite.dat %{buildroot}/usr/local/xrayr/geosite.dat
install -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}/usr/local/xrayr/README.md
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}/usr/local/xrayr/LICENSE
install -m 644 %{_builddir}/%{name}-%{version}/config.yml.example %{buildroot}%{_sysconfdir}/xrayr/config.yml.example
install -m 644 %{_builddir}/%{name}-%{version}/xrayr.service %{buildroot}%{_sysconfdir}/systemd/system

%post
ln -s /usr/local/xrayr/xrayr %{_bindir}/xrayr

%postun
rm -f %{_bindir}/xrayr

%clean
rm -rf %{buildroot}

%files
%attr(0755, root, root) /usr/local/xrayr
%attr(0755, root, root) /usr/local/xrayr/xrayr
%attr(0644, root, root) /usr/local/xrayr/dns.json
%attr(0644, root, root) /usr/local/xrayr/route.json
%attr(0644, root, root) /usr/local/xrayr/custom_outbound.json
%attr(0644, root, root) /usr/local/xrayr/custom_inbound.json
%attr(0644, root, root) /usr/local/xrayr/rulelist
%attr(0644, root, root) /usr/local/xrayr/geoip.dat
%attr(0644, root, root) /usr/local/xrayr/geosite.dat
%attr(0644, root, root) /usr/local/xrayr/README.md
%attr(0644, root, root) /usr/local/xrayr/LICENSE
%attr(0644, root, root) %{_sysconfdir}/xrayr
%attr(0644, root, root) %{_sysconfdir}/xrayr/config.yml.example
%attr(0644, root, root) %{_sysconfdir}/systemd/system/xrayr.service

%changelog
* Sun Jul 24 2022 The NeXT Project Team <package@nextpanel.dev> - 0.9.0-1
 - https://github.com/XrayR-project/XrayR/releases/tag/v0.9.0
