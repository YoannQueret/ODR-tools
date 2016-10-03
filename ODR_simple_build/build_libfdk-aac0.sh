#!/bin/bash

BUILD_DIR="/tmp/build-ODR/"
PKG_DIR="/tmp/build-ODR/pkg/"
RUN_DIR=$(dirname $(readlink -f $0))

DEB_VERSION="jessie"
ARCH="amd64"
PKG_NAME="libfdk-aac0"

mkdir -p ${BUILD_DIR}
mkdir -p ${PKG_DIR}

### Retreive source from GIT
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/fdk-aac.git
cd fdk-aac/

VERSION=`grep AC_INIT configure.ac | sed -E 's/.*\[([0-9.]+)\].*/\1/'`
GIT_HASH=`git log --pretty=format:'%h' -n 1`
PKG_VERSION="${VERSION}+dab1-${GIT_HASH}"
DESTDIR="${PKG_DIR}/${PKG_NAME}-${PKG_VERSION}~${DEB_VERSION}_${ARCH}/"

./bootstrap
./configure
make
make install
make install DESTDIR=${DESTDIR}



cp -r ${RUN_DIR}/${PKG_NAME}/DEBIAN/ "${DESTDIR}"
sed "s/##PACKAGE##/${PKG_NAME}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
sed "s/##VERSION##/${PKG_VERSION}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
cd ${PKG_DIR}/
dpkg-deb --build ${DESTDIR}