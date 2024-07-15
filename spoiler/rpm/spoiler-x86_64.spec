Name:           spoiler
Version:        0.0.1
Release:        1%{?dist}
Summary:        Yet another proxy backend server for the illegal industry.
Group:          Unspecified
License:        GPL-3.0
URL:            https://github.com/SagerNet/spoiler
Packager:       The NeXT Project Team <package@sspanel.org>
BuildRequires:  systemd

%description
Yet another proxy backend server for the illegal industry.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/spoiler
mkdir -p %{buildroot}%{_sysconfdir}/spoiler
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{_builddir}/%{name}-%{version}/spoiler-amd64-linux %{buildroot}/usr/local/spoiler/spoiler
install -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}/usr/local/spoiler/README.md
install -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}/usr/local/spoiler/LICENSE
install -m 644 %{_builddir}/%{name}-%{version}/config.json %{buildroot}%{_sysconfdir}/spoiler/config.json
install -m 644 %{_builddir}/%{name}-%{version}/spoiler.service %{buildroot}%{_sysconfdir}/systemd/system

%post
ln -s /usr/local/spoiler/spoiler %{_bindir}/spoiler

%postun
rm -f %{_bindir}/spoiler

%clean
rm -rf %{buildroot}

%files
%attr(0755, root, root) /usr/local/spoiler
%attr(0755, root, root) /usr/local/spoiler/spoiler
%attr(0644, root, root) /usr/local/spoiler/README.md
%attr(0644, root, root) /usr/local/spoiler/LICENSE
%attr(0644, root, root) %{_sysconfdir}/spoiler
%attr(0644, root, root) %{_sysconfdir}/spoiler/config.json
%attr(0644, root, root) %{_sysconfdir}/systemd/system/spoiler.service

%changelog
* Sun Jul 24 2022 The NeXT Project Team <package@sspanel.org> - 1.0.0-1
 - https://github.com/SagerNet/spoiler/releases/tag/v1.0.0
