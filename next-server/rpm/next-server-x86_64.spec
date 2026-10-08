Name:           next-server
Version:        0.0.1
Release:        1%{?dist}
Summary:        NeXT-Panel node server, built on sing-box.
Group:          Unspecified
License:        GPL-3.0
URL:            https://github.com/The-NeXT-Project/NeXT-Server
Packager:       The NeXT Project Team <package@nextpanel.dev>
BuildRequires:  systemd

# The binary is static and already stripped.
%global debug_package %{nil}

%description
NeXT-Panel node server, built on sing-box.

%install
# The build passes the staged files in with --define "srcdir ...", since
# _builddir changed layout in rpm 4.20.
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/next-server
mkdir -p %{buildroot}%{_sysconfdir}/next-server
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{srcdir}/next-server-amd64-linux %{buildroot}/usr/local/next-server/next-server
install -m 644 %{srcdir}/README.md %{buildroot}/usr/local/next-server/README.md
install -m 644 %{srcdir}/CHANGELOG.md %{buildroot}/usr/local/next-server/CHANGELOG.md
install -m 644 %{srcdir}/LICENSE %{buildroot}/usr/local/next-server/LICENSE
install -m 644 %{srcdir}/config.json %{buildroot}%{_sysconfdir}/next-server/config.json.example
install -m 644 %{srcdir}/next-server.service %{buildroot}%{_sysconfdir}/systemd/system/next-server.service
ln -s ../local/next-server/next-server %{buildroot}%{_bindir}/next-server

# 1.x reads /etc/next-server/config.json, 0.x read config.yml. Refuse an
# upgrade from 0.x until the new configuration is in place, so that a routine
# update cannot leave a node that fails on its next restart.
%pre
if [ "$1" -gt 1 ] && [ -f %{_sysconfdir}/next-server/config.yml ] && [ ! -f %{_sysconfdir}/next-server/config.json ]; then
	echo "next-server: 1.x needs %{_sysconfdir}/next-server/config.json, see" >&2
	echo "next-server: https://github.com/The-NeXT-Project/NeXT-Server/blob/main/CHANGELOG.md" >&2
	echo "next-server: keeping the installed version; write the new configuration, then update again" >&2
	exit 1
fi

%post
if [ -d /run/systemd/system ]; then
	systemctl daemon-reload >/dev/null 2>&1 || :
	# On an upgrade, a running server switches to the new binary.
	if [ "$1" -gt 1 ] && [ -f %{_sysconfdir}/next-server/config.json ]; then
		systemctl try-restart next-server.service >/dev/null 2>&1 || :
	fi
fi

# 0.x removed /usr/bin/next-server in its %%postun, which runs after this
# package is installed; put the link back once the upgrade is done.
%posttrans
[ -e %{_bindir}/next-server ] || ln -s ../local/next-server/next-server %{_bindir}/next-server

%preun
if [ "$1" -eq 0 ] && [ -d /run/systemd/system ]; then
	systemctl --no-reload disable --now next-server.service >/dev/null 2>&1 || :
fi

%postun
if [ "$1" -eq 0 ] && [ -d /run/systemd/system ]; then
	systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%dir %attr(0755, root, root) /usr/local/next-server
%attr(0755, root, root) /usr/local/next-server/next-server
%attr(0644, root, root) /usr/local/next-server/README.md
%attr(0644, root, root) /usr/local/next-server/CHANGELOG.md
%attr(0644, root, root) /usr/local/next-server/LICENSE
%{_bindir}/next-server
%dir %attr(0755, root, root) %{_sysconfdir}/next-server
%attr(0644, root, root) %{_sysconfdir}/next-server/config.json.example
%attr(0644, root, root) %{_sysconfdir}/systemd/system/next-server.service

%changelog
* Thu Oct 08 2026 The NeXT Project Team <package@nextpanel.dev> - 1.0.0-1
 - NeXT-Server 1.x, built on sing-box; reads /etc/next-server/config.json
* Sat Dec 23 2023 The NeXT Project Team <package@nextpanel.dev> - 0.0.0-1
 - Initial release
