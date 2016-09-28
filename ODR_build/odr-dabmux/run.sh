# Install build tools
apt -y -f install devscripts automake build-essential

# Install build dependancies
apt -y -f install debhelper dh-autoreconf libboost-system-dev libboost-thread-dev libboost-regex-dev libzmq3-dev libcurl4-gnutls-dev libfftw3-dev libfec


cd /tmp/odr-dabmux/pkg/
uscan --download-current-version
tar -f ../odr-dabmux-*.tar.gz -x --strip-components=1
dpkg-buildpackage
