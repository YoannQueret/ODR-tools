#!/bin/bash

BUILD_DIR="/tmp/build-ODR/"
PKG_DIR="/tmp/build-ODR/pkg/"
RUN_DIR=$(dirname $(readlink -f $0))

DEB_VERSION="jessie"
ARCH="amd64"
PKG_NAME="libuhd"

mkdir -p ${BUILD_DIR}
mkdir -p ${PKG_DIR}

### Building package for UHD
UHD_RELEASE="release_003_008_002"
#UHD_RELEASE="release_003_007_000"


VERSION=${UHD_RELEASE//_0/_}
VERSION=${VERSION//_0/_}
VERSION=${VERSION#release_*}
VERSION=${VERSION//_/.}

PKG_NAME_VERSION=${UHD_RELEASE#release_*}
PKG_NAME_VERSION=${PKG_NAME_VERSION//_/-}

PKG_NAME_SPE="${PKG_NAME}-${PKG_NAME_VERSION}"

cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/uhd.git
cd uhd/
git checkout ${UHD_RELEASE}

GIT_HASH=`git log --pretty=format:'%h' -n 1`
PKG_VERSION="${VERSION}"
DESTDIR="${PKG_DIR}/${PKG_NAME_SPE}-${PKG_VERSION}~${GIT_HASH}_${DEB_VERSION}_${ARCH}/"

mkdir build
cd build
cmake ../host
make
make test
make install DESTDIR=${DESTDIR}


cp -r ${RUN_DIR}/${PKG_NAME}/DEBIAN/ "${DESTDIR}"
sed "s/##PACKAGE##/${PKG_NAME_SPE}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
sed "s/##VERSION##/${PKG_VERSION}/g" "${DESTDIR}/DEBIAN/control" > /tmp/control && mv /tmp/control "${DESTDIR}/DEBIAN/control"
cd ${PKG_DIR}/
dpkg-deb --build ${DESTDIR}