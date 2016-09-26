#!/bin/bash

BUILD_DIR="/tmp/build-ODR/"
PKG_DIR="/tmp/build-ODR/pkg/"
RUN_DIR=$(dirname $(readlink -f $0))

DEB_VERSION="jessie"
ARCH="amd64"

mkdir -p ${BUILD_DIR}
mkdir -p ${PKG_DIR}

### Building package for fdk-aac
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/ODR-DabMux.git
cd ODR-DabMux/
VERSION=`git describe --tags`
VERSION=${VERSION#v*}
./bootstrap.sh
./configure --enable-output-raw --enable-input-udp
make
make install DESTDIR=${PKG_DIR}/ODR-DabMux-${VERSION}~${DEB_VERSION}_${ARCH}/



cp -r ${RUN_DIR}/ODR-DabMux/DEBIAN/ "${PKG_DIR}/ODR-DabMux-${VERSION}~${DEB_VERSION}_${ARCH}/"
sed "s/##VERSION##/${VERSION}/g" "${PKG_DIR}/ODR-DabMux-${VERSION}~${DEB_VERSION}_${ARCH}/DEBIAN/control" > /tmp/control && mv /tmp/control "${PKG_DIR}/ODR-DabMux-${VERSION}~${DEB_VERSION}_${ARCH}/DEBIAN/control"
cd ${PKG_DIR}/
dpkg-deb --build ODR-DabMux-${VERSION}~${DEB_VERSION}_${ARCH}