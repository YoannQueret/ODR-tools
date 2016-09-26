#!/bin/bash

BUILD_DIR="/tmp/build-ODR/"
PKG_DIR="/tmp/build-ODR/pkg/"
RUN_DIR=$(dirname $(readlink -f $0))

DEB_VERSION="jessie"
ARCH="amd64"
PKG_NAME="odr-audioenc"

mkdir -p ${BUILD_DIR}
mkdir -p ${PKG_DIR}

### Building package for fdk-aac
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/ODR-AudioEnc.git
cd ODR-AudioEnc/

VERSION=`git describe --tags`
VERSION=${VERSION#v*}
GIT_HASH=`git log --pretty=format:'%h' -n 1`
PKG_VERSION="${VERSION}+${GIT_HASH}"
DESTDIR="${PKG_DIR}/${PKG_NAME}-${PKG_VERSION}~${DEB_VERSION}_${ARCH}/"

./bootstrap
./configure --enable-jack --enable-vlc --enable-alsa
make
make install DESTDIR=${DESTDIR}



cp -r ${RUN_DIR}/odr-audioenc/DEBIAN/ "${DESTDIR}"
sed "s/##PACKAGE##/${PKG_NAME}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
sed "s/##VERSION##/${PKG_VERSION}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
cd ${PKG_DIR}/
dpkg-deb --build ${DESTDIR}