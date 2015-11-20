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
git clone https://github.com/Opendigitalradio/fdk-aac-dabplus.git
cd fdk-aac-dabplus/
./bootstrap
./configure --enable-jack --enable-vlc
make
make install

apt-get --force-yes -y install python-zmq

cd /usr/src/
git clone https://github.com/Opendigitalradio/ODR-DabMux.git
cd ODR-DabMux/
./bootstrap.sh
./configure --enable-input-zeromq --enable-input-prbs --enable-input-slip --enable-input-udp --enable-output-zeromq --enable-output-raw --enable-output-edi --enable-format-bridge
make
make install

apt-get --force-yes -y install libboost-all-dev libusb-1.0-0-dev python-cheetah doxygen python-docutils cmake libudev-dev libuhd-dev libfftw3-dev

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

apt-get --force-yes -y install sudo

cd ~
git clone https://github.com/Opendigitalradio/dab-scripts.git
cd dab-scripts/
mv examplesite/ site
mkdir site/slide
wget "https://gist.githubusercontent.com/YoannQueret/6c719979d64a2deadf75/raw/6811faee12706f429b37e63758e13b32b5ab6cc2/run.sh" -O run.sh
