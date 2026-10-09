Name:           realm
Version:        0.0.1
Release:        1%{?dist}
Summary:        A network relay tool
Group:          Unspecified
License:        MIT
URL:            https://github.com/zhboner/realm
Packager:       The NeXT Project Team <package@nextpanel.dev>
BuildRequires:  systemd

%description
A network relay tool

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/realm
mkdir -p %{buildroot}%{_sysconfdir}/realm
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/%{name}-%{version}/realm-amd64-linux %{buildroot}/usr/local/realm/realm
install -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}/usr/local/realm/README.md
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}/usr/local/realm/LICENSE
install -m 644 %{_builddir}/%{name}-%{version}/config.toml.example %{buildroot}%{_sysconfdir}/realm/config.toml.example
install -m 644 %{_builddir}/%{name}-%{version}/realm.service %{buildroot}%{_sysconfdir}/systemd/system

%post
ln -s /usr/local/realm/realm %{_bindir}/realm

%postun
rm -f %{_bindir}/realm

%clean
rm -rf %{buildroot}

%files
%attr(0755, root, root) /usr/local/realm
%attr(0755, root, root) /usr/local/realm/realm
%attr(0644, root, root) /usr/local/realm/README.md
%attr(0644, root, root) /usr/local/realm/LICENSE
%attr(0644, root, root) %{_sysconfdir}/realm
%attr(0644, root, root) %{_sysconfdir}/realm/config.toml.example
%attr(0644, root, root) %{_sysconfdir}/systemd/system/realm.service

%changelog
* Tue Oct 07 2025 The NeXT Project Team <package@nextpanel.dev> - 0.0.0-1
 - Initial release
