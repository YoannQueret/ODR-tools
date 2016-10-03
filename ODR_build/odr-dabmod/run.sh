# Install build tools
apt -y -f install devscripts fakeroot automake build-essential

# Install build dependancies
apt -y -f install debhelper dh-autoreconf libboost-system-dev libboost-thread-dev libzmq3-dev libuhd-dev libfftw3-dev libcurl4-gnutls-dev


cd /tmp/odr-dabmod/pkg/
uscan --download-current-version
tar -f ../odr-dabmod-*.tar.gz -x --strip-components=1
dpkg-buildpackage
