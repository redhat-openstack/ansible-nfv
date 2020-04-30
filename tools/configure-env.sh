#!/bin/bash

set -e

# Validated in Fedora28

DIR=$(dirname $(readlink -f $0))/..

if ! `which virtualenv-3 > /dev/null`; then
    echo 'Installing python virtualenv'
    yum install -y python3-virtualenv
fi

if ! `which python3 > /dev/null`; then
    echo 'Installing python3'
    yum install -y python3
fi

if ! `which pip3 > /dev/null`; then
    echo 'Installing pip3'
    echo 'command pending, exiting...'
    exit 1
fi

VENV=$DIR/.venv
if [ ! -d $VENV ]; then
    virtualenv-3 $VENV >/dev/null
fi

source $VENV/bin/activate

sudo yum -y install qemu libvirt libxslt-devel libxml2-devel libvirt-devel libguestfs-tools-c ruby-devel gcc
if ! `which vagrant > /dev/null`; then
    echo 'Installing vagrant 2.2.7 version'
    sudo yum -y install https://releases.hashicorp.com/vagrant/2.2.7/vagrant_2.2.7_x86_64.rpm
fi

vagrant plugin install vagrant-libvirt

sudo systemctl start libvirtd
pip3 install -r $DIR/molecule-requirements.txt

