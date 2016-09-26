#!/bin/bash

BUILD_DIR="/tmp/build-ODR/"
PKG_DIR="/tmp/build-ODR/pkg/"

DEB_VERSION="jessie"
ARCH="amd64"

mkdir -p ${BUILD_DIR}
mkdir -p ${PKG_DIR}

### Building package for ka9q-fec
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/ka9q-fec.git
cd ka9q-fec/
VERSION=`git describe --tags`
./bootstrap
./configure
make
make install
make install DESTDIR=${PKG_DIR}/libodr-fec-${VERSION}~${DEB_VERSION}_${ARCH}/



### Building package for fdk-aac
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/fdk-aac.git
cd fdk-aac/
VERSION=`git describe --tags`
./bootstrap
./configure
make
make install
make install DESTDIR=${PKG_DIR}/libodr-fdk-aac-${VERSION}~${DEB_VERSION}_${ARCH}/



### Building package for ODR-AudioEnc
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/ODR-AudioEnc.git
cd ODR-AudioEnc/
VERSION=`git describe --tags`
./bootstrap
./configure --enable-jack --enable-vlc --enable-alsa
make
make install DESTDIR=${PKG_DIR}/ODR-AudioEnc-${VERSION}~${DEB_VERSION}_${ARCH}/



### Building package for ODR-DabMux
cd ${BUILD_DIR}
git clone https://github.com/Opendigitalradio/ODR-DabMux.git
cd ODR-DabMux/
VERSION=`git describe --tags`
./bootstrap.sh
./configure --enable-output-raw --enable-input-udp
make
make install DESTDIR=${PKG_DIR}/ODR-DabMux-${VERSION}~${DEB_VERSION}_${ARCH}/