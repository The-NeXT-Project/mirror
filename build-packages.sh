# Builds a product's deb and rpm packages in one Jenkins job and publishes
# them to the mirror's repository directory. The job checks out the product,
# then sources this file after setting:
#   PKG      package name, also the mirror directory with its control files
#   RELEASE  version without the leading v; the commit hash is appended
#   EXAMPLE  example configuration in the checkout, installed as
#            /etc/$PKG/<its name>.example
#   build    a function that builds the binary for $GOARCH into "$1"
# and optionally:
#   EXAMPLE_NAME  the name to install EXAMPLE under instead
#   README        the checkout's readme, README.md by default; packaged as README.md
#   prepare       a function run before the builds, instead of `go mod download`
#
#   PKG=sing-box
#   RELEASE=$(git describe --tags --abbrev=0 | sed -e "s/^v//")
#   EXAMPLE=release/config/config.json
#   build() { go build -v -trimpath -ldflags "-s -w -buildid=" -o "$1" ./cmd/sing-box; }
#   wget -q https://raw.githubusercontent.com/The-NeXT-Project/mirror/main/build-packages.sh -O build-packages.sh
#   . ./build-packages.sh

MIRROR_URL=https://raw.githubusercontent.com/The-NeXT-Project/mirror/main/$PKG
REPO_DIR=${REPO_DIR:-$HOME/workspace/next-mirror-upload/mirror/repo}
# Each rpm repository directory and the dist tag its file names carry.
RPM_REPOS="fedora/44:fc44 fedora/43:fc43 rhel/9:el9 rhel/10:el10"

HEAD=$(git rev-parse --short HEAD)
VERSION=$RELEASE.g$HEAD
WORKSPACE_DIR=$(pwd)
OUT=$WORKSPACE_DIR/out
if [ -z "$EXAMPLE_NAME" ]; then
	EXAMPLE_NAME=${EXAMPLE##*/}
	EXAMPLE_NAME=${EXAMPLE_NAME%.example}.example
fi
README=${README:-README.md}
RPM_SRC=$WORKSPACE_DIR/rpmbuild/BUILD/$PKG-$VERSION

rm -rf out pkg rpmbuild
mkdir -p out pkg rpmbuild/SPECS "$RPM_SRC"

if type prepare >/dev/null 2>&1; then
	prepare
else
	go mod download
fi

for file in $PKG.service deb/amd64.control deb/arm64.control deb/riscv64.control deb/copyright deb/rules; do
	wget -q "$MIRROR_URL/$file" -O "pkg/$(basename $file)"
done
for ARCH in x86_64 aarch64; do
	wget -q "$MIRROR_URL/rpm/$PKG-$ARCH.spec" -O "rpmbuild/SPECS/$PKG-$ARCH.spec"
done

# Binaries, once for both package formats.
export GOOS=linux CGO_ENABLED=0
for ARCH in amd64 arm64 riscv64; do
	if [ "$ARCH" = amd64 ]; then
		export GOAMD64=v3
	else
		unset GOAMD64
	fi
	GOARCH=$ARCH build "$OUT/$PKG-$ARCH-linux"
done
unset GOOS GOARCH GOAMD64 CGO_ENABLED

# deb
for ARCH in amd64 arm64 riscv64; do
	DIR=pkg/$PKG-$ARCH
	mkdir -p $DIR/DEBIAN $DIR/etc/$PKG $DIR/etc/systemd/system $DIR/usr/local/$PKG
	sed -e "s/Version: 0.0.1/Version: $VERSION/" pkg/$ARCH.control > $DIR/DEBIAN/control
	cp pkg/copyright pkg/rules $DIR/DEBIAN/
	install -m 0755 out/$PKG-$ARCH-linux $DIR/usr/local/$PKG/$PKG
	cp "$README" $DIR/usr/local/$PKG/README.md
	cp LICENSE $DIR/usr/local/$PKG/
	cp "$EXAMPLE" "$DIR/etc/$PKG/$EXAMPLE_NAME"
	cp pkg/$PKG.service $DIR/etc/systemd/system/
	dpkg-deb --root-owner-group --build $DIR out/${PKG}_${VERSION}-1_$ARCH.deb
done

# rpm; the specs install from %{_builddir}/%{name}-%{version}.
cp out/$PKG-amd64-linux out/$PKG-arm64-linux LICENSE pkg/$PKG.service "$RPM_SRC/"
cp "$README" "$RPM_SRC/README.md"
cp "$EXAMPLE" "$RPM_SRC/$EXAMPLE_NAME"
for ARCH in x86_64 aarch64; do
	sed -i -e "s/^Version:        0.0.1$/Version:        $VERSION/" rpmbuild/SPECS/$PKG-$ARCH.spec
	rpmbuild --define "_topdir $WORKSPACE_DIR/rpmbuild" -bb --target=$ARCH rpmbuild/SPECS/$PKG-$ARCH.spec
	# The build host's own %{dist}, if any, is in the built name.
	cp rpmbuild/RPMS/$ARCH/$PKG-$VERSION-1*.$ARCH.rpm out/$PKG-$VERSION-1.$ARCH.rpm
done

# Publish only now that every package is built, so a failed build leaves
# the previous packages in place.
mkdir -p $REPO_DIR/deb/pool/main
for ARCH in amd64 arm64 riscv64; do
	mkdir -p $REPO_DIR/deb/dists/stable/main/binary-$ARCH
done
rm -f $REPO_DIR/deb/pool/main/${PKG}_*
cp out/${PKG}_${VERSION}-1_*.deb $REPO_DIR/deb/pool/main/

for REPO in $RPM_REPOS; do
	for ARCH in x86_64 aarch64; do
		DIR=$REPO_DIR/${REPO%%:*}/$ARCH
		mkdir -p $DIR
		rm -f $DIR/$PKG-[0-9]*
		cp out/$PKG-$VERSION-1.$ARCH.rpm $DIR/$PKG-$VERSION-1.${REPO##*:}.$ARCH.rpm
	done
done
