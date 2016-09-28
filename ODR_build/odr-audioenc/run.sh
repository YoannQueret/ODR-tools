# Install build tools
apt -y -f install devscripts fakeroot automake build-essential

# Install build dependancies
apt -y -f install debhelper dh-autoreconf libzmq3-dev libavresample-dev libresample1-dev libfdk-aac0 libvlc-dev libasound2-dev libjack-dev


cd /tmp/odr-audioenc/pkg/
uscan --download-current-version
tar -f ../odr-audioenc-*.tar.gz -x --strip-components=1
dpkg-buildpackage
