#!/bin/bash

apt install --force-yes -y automake build-essential libtool libboost-system-dev libboost-thread-dev libzmq3-dev libcurl4-gnutls-dev libuhd-dev libfftw3-dev

BUILD_DIR="/tmp/build-ODR/"
PKG_DIR="/tmp/build-ODR/pkg/"
RUN_DIR=$(dirname $(readlink -f $0))

DEB_VERSION="jessie"
ARCH="amd64"
PKG_NAME="odr-dabmod"

mkdir -p ${BUILD_DIR}
mkdir -p ${PKG_DIR}

### Building package for fdk-aac
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/ODR-DabMod.git
cd ODR-DabMod/

VERSION=`git describe --tags`
VERSION=${VERSION#v*}
GIT_HASH=`git log --pretty=format:'%h' -n 1`
PKG_VERSION="${VERSION}"
DESTDIR="${PKG_DIR}/${PKG_NAME}-${PKG_VERSION}~${GIT_HASH}_${DEB_VERSION}_${ARCH}/"

./bootstrap.sh
./configure --enable-zeromq --enable-fft-simd --enable-output-uhd
make
make install DESTDIR=${DESTDIR}



cp -r ${RUN_DIR}/${PKG_NAME}/DEBIAN/ "${DESTDIR}"
sed "s/##PACKAGE##/${PKG_NAME}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
sed "s/##VERSION##/${PKG_VERSION}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
cd ${PKG_DIR}/
dpkg-deb --build ${DESTDIR}