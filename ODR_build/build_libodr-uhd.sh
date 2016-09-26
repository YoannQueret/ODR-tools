#!/bin/bash

BUILD_DIR="/tmp/build-ODR/"
PKG_DIR="/tmp/build-ODR/pkg/"
RUN_DIR=$(dirname $(readlink -f $0))

DEB_VERSION="jessie"
ARCH="amd64"

mkdir -p ${BUILD_DIR}
mkdir -p ${PKG_DIR}

# ### Building package for UHD
#UHD_RELEASE="release_003_008_002"
UHD_RELEASE="release_003_007_000"
VERSION="3.7.0"

cd ${BUILD_DIR}
git clone git://github.com/EttusResearch/uhd.git
cd uhd/
git checkout ${UHD_RELEASE}
mkdir build
cd build
cmake ../host
make
make test
make install DESTDIR=${PKG_DIR}/libodr-uhd-${VERSION}~${DEB_VERSION}_${ARCH}/


cp -r ${RUN_DIR}/libodr-uhd/DEBIAN/ "${PKG_DIR}/libodr-uhd-${VERSION}~${DEB_VERSION}_${ARCH}/"
sed "s/##VERSION##/${VERSION}/g" "${PKG_DIR}/libodr-uhd-${VERSION}~${DEB_VERSION}_${ARCH}/DEBIAN/control" > /tmp/control && mv /tmp/control "${PKG_DIR}/libodr-uhd-${VERSION}~${DEB_VERSION}_${ARCH}/DEBIAN/control"
cd ${PKG_DIR}/
dpkg-deb --build libodr-uhd-${VERSION}~${DEB_VERSION}_${ARCH}