#!/bin/bash

# Install ODR on a debian jessie
# This script must be run as superuser

#------------------------------------
# /!\ You need to add deb-multimedia repository to have the lastest mplayer version with resampler functions running
# echo "deb http://www.deb-multimedia.org jessie main non-free" >> /etc/apt/sources.list
# apt-get update
# apt-get --force-yes -y install deb-multimedia-keyring
# apt-get update
#------------------------------------


apt-get --force-yes -y install htop iftop vim net-tools sysstat mtr-tiny screen ca-certificates
apt-get --force-yes -y install git automake build-essential

apt-get --force-yes -y install libsodium-dev libzmq3-dev libzmq3

# Zeromq not need to be installed from source with debian Jessie
#cd /usr/src/
#wget http://download.zeromq.org/zeromq-4.0.4.tar.gz
#tar zxvf zeromq-4.0.4.tar.gz
#cd zeromq-4.0.4
#./configure --enable-shared
#make
#make install

cd /usr/src/
git clone https://github.com/Opendigitalradio/ka9q-fec.git
cd ka9q-fec/
./bootstrap
./configure
make
make install

apt-get --force-yes -y install libboost-thread-dev libboost-system-dev libmagickwand-dev libasound2-dev jackd2 libjack-jackd2-dev mplayer libavresample2 libsamplerate0 libvlc-dev vlc alsa-base alsa-utils

cd /usr/src/
git clone https://github.com/Opendigitalradio/fdk-aac.git
cd fdk-aac/
./bootstrap
./configure
make
make install
ldconfig

cd /usr/src/
git clone https://github.com/Opendigitalradio/ODR-AudioEnc.git
cd ODR-AudioEnc/
./bootstrap
./configure --enable-jack --enable-vlc --enable-alsa
make
make install

cd /usr/src/
git clone https://github.com/Opendigitalradio/ODR-PadEnc.git
cd ODR-PadEnc/
./bootstrap
./configure
make
make install

apt-get --force-yes -y install python-zmq libcurl4-gnutls-dev libboost-regex-dev

cd /usr/src/
git clone https://github.com/Opendigitalradio/ODR-DabMux.git
cd ODR-DabMux/
./bootstrap.sh
./configure --enable-input-prbs --enable-input-slip --enable-output-raw --enable-output-edi
make
make install

apt-get --force-yes -y install libboost-all-dev libusb-1.0-0-dev python-cheetah doxygen python-docutils cmake libudev-dev libuhd-dev libfftw3-dev

# 3.7 For MFM
# 3.8.2 For SFN - juste use release_003_008_002 instead release_003_007_000
cd /usr/src/
git clone git://github.com/EttusResearch/uhd.git
cd uhd/
git checkout release_003_007_000
mkdir build
cd build
cmake ../host
make
make test
make install
ldconfig

uhd_images_downloader
uhd_find_devices

cd /usr/src/
git clone https://github.com/Opendigitalradio/ODR-DabMod.git
cd ODR-DabMod/
./bootstrap.sh
./configure --enable-zeromq --enable-fft-simd --enable-output-uhd
make
make install


