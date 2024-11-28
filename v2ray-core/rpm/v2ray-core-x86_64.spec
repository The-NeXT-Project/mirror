Name:           v2ray-core
Version:        0.0.1
Release:        1%{?dist}
Summary:        A platform for building proxies to bypass network restrictions.
Group:          Unspecified
License:        MIT
URL:            https://github.com/v2fly/v2ray-core
Packager:       The NeXT Project Team <package@nextpanel.dev>
BuildRequires:  systemd

%description
A platform for building proxies to bypass network restrictions.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/v2ray-core
mkdir -p %{buildroot}%{_sysconfdir}/v2ray-core
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/%{name}-%{version}/v2ray-core-amd64-linux %{buildroot}/usr/local/v2ray-core/v2ray-core
install -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}/usr/local/v2ray-core/README.md
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}/usr/local/v2ray-core/LICENSE
install -m 644 %{_builddir}/%{name}-%{version}/config.json.example %{buildroot}%{_sysconfdir}/v2ray-core/config.json.example
install -m 644 %{_builddir}/%{name}-%{version}/v2ray-core.service %{buildroot}%{_sysconfdir}/systemd/system

%post
ln -s /usr/local/v2ray-core/v2ray-core %{_bindir}/v2ray-core

%postun
rm -f %{_bindir}/v2ray-core

%clean
rm -rf %{buildroot}

%files
%attr(0755, root, root) /usr/local/v2ray-core
%attr(0755, root, root) /usr/local/v2ray-core/v2ray-core
%attr(0644, root, root) /usr/local/v2ray-core/README.md
%attr(0644, root, root) /usr/local/v2ray-core/LICENSE
%attr(0644, root, root) %{_sysconfdir}/v2ray-core
%attr(0644, root, root) %{_sysconfdir}/v2ray-core/config.json.example
%attr(0644, root, root) %{_sysconfdir}/systemd/system/v2ray-core.service

%changelog
* Sun Nov 28 2024 The NeXT Project Team <package@nextpanel.dev> - 0.0.0-1
 - Initial release
