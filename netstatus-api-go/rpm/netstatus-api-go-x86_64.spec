Name:           netstatus-api-go
Version:        0.0.1
Release:        1%{?dist}
Summary:        NetStatus API (Go Edition)
Group:          Unspecified
License:        GPL-3.0
URL:            https://github.com/The-NeXT-Project/NetStatus-API-Go
Packager:       The NeXT Project Team <package@nextpanel.dev>
BuildRequires:  systemd

%description
NetStatus API (Go Edition)

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/netstatus-api-go
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/%{name}-%{version}/netstatus-api-go-amd64-linux %{buildroot}/usr/local/netstatus-api-go/netstatus-api-go
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}/usr/local/netstatus-api-go/LICENSE
install -m 644 %{_builddir}/%{name}-%{version}/netstatus-api-go.service %{buildroot}%{_sysconfdir}/systemd/system

%post
ln -s /usr/local/netstatus-api-go/netstatus-api-go %{_bindir}/netstatus-api-go

%postun
rm -f %{_bindir}/netstatus-api-go

%clean
rm -rf %{buildroot}

%files
%attr(0755, root, root) /usr/local/netstatus-api-go
%attr(0755, root, root) /usr/local/netstatus-api-go/netstatus-api-go
%attr(0644, root, root) /usr/local/netstatus-api-go/LICENSE
%attr(0644, root, root) %{_sysconfdir}/systemd/system/netstatus-api-go.service

%changelog
* Sun Dec 23 2023 The NeXT Project Team <package@nextpanel.dev> - 0.0.1-1
 - https://github.com/The-NeXT-Project/NetStatus-API-Go/releases/tag/v0.0.1
