#!/bin/bash

apt install --force-yes -y automake build-essential

BUILD_DIR="/tmp/build-ODR/"
PKG_DIR="/tmp/build-ODR/pkg/"
RUN_DIR=$(dirname $(readlink -f $0))

DEB_VERSION="jessie"
ARCH="amd64"
PKG_NAME="libfec"

mkdir -p ${BUILD_DIR}
mkdir -p ${PKG_DIR}

### Building package for ka9q-fec
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/ka9q-fec.git
cd ka9q-fec/

VERSION=`git describe --tags`
VERSION=${VERSION#v*}
VERSION=${VERSION%%-*}
GIT_HASH=`git log --pretty=format:'%h' -n 1`
PKG_VERSION="${VERSION}+odr1-${GIT_HASH}"
DESTDIR="${PKG_DIR}/${PKG_NAME}-${PKG_VERSION}~${DEB_VERSION}_${ARCH}/"

./bootstrap
./configure
make
make install DESTDIR=${DESTDIR}


cp -r ${RUN_DIR}/${PKG_NAME}/debian/ "${DESTDIR}"
sed "s/##PACKAGE##/${PKG_NAME}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
sed "s/##VERSION##/${PKG_VERSION}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
cd ${PKG_DIR}/
dpkg-deb --build ${DESTDIR}