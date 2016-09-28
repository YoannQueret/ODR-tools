#!/bin/bash

PKG="odr-dabmod"

BUILD_IP="192.168.40.122"
PUB_KEY="/home/yoann/.ssh/id_dsa_yoann.pub"

echo "== Try to build ${PKG} on ${BUILD_IP} =="

echo "> Copy ssh public key on remote build server ${BUILD_IP}"
ssh-copy-id -i ${PUB_KEY} root@${BUILD_IP}

echo "> Remove existing files on remote build server ${BUILD_IP}"
ssh -i ${PUB_KEY} root@${BUILD_IP} "rm -Rf /tmp/${PKG}/"

echo "> Copy files on remote build server ${BUILD_IP}"
scp -i ${PUB_KEY} -r ./${PKG}/ root@${BUILD_IP}:/tmp/

echo "> Run build script ..."
ssh -i ${PUB_KEY} root@${BUILD_IP} "bash /tmp/${PKG}/run.sh > /tmp/${PKG}/run.log"
