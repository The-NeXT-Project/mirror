Name:           clash-meta
Version:        0.0.1
Release:        1%{?dist}
Summary:        Another Clash Kernel.
Group:          Unspecified
License:        GPL-3.0
URL:            https://github.com/MetaCubeX/mihomo
Packager:       The NeXT Project Team <package@nextpanel.dev>
BuildRequires:  systemd

%description
Another Clash Kernel.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/clash-meta
mkdir -p %{buildroot}%{_sysconfdir}/clash-meta
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/%{name}-%{version}/clash-meta-amd64-linux %{buildroot}/usr/local/clash-meta/clash-meta
install -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}/usr/local/clash-meta/README.md
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}/usr/local/clash-meta/LICENSE
install -m 644 %{_builddir}/%{name}-%{version}/config.yaml %{buildroot}%{_sysconfdir}/clash-meta/config.yaml.example
install -m 644 %{_builddir}/%{name}-%{version}/clash-meta.service %{buildroot}%{_sysconfdir}/systemd/system

%post
ln -s /usr/local/clash-meta/clash-meta %{_bindir}/clash-meta

%postun
rm -f %{_bindir}/clash-meta

%clean
rm -rf %{buildroot}

%files
%attr(0755, root, root) /usr/local/clash-meta
%attr(0755, root, root) /usr/local/clash-meta/clash-meta
%attr(0644, root, root) /usr/local/clash-meta/README.md
%attr(0644, root, root) /usr/local/clash-meta/LICENSE
%attr(0644, root, root) %{_sysconfdir}/clash-meta
%attr(0644, root, root) %{_sysconfdir}/clash-meta/config.yaml.example
%attr(0644, root, root) %{_sysconfdir}/systemd/system/clash-meta.service

%changelog
* Sun Nov 28 2024 The NeXT Project Team <package@nextpanel.dev> - 0.0.0-1
 - Initial release
