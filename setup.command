#!/bin/bash
cd -- "$(dirname -- "$0")"
export PATH=$PATH:$(dirname -- "$0")
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
rm -rf get-pip.py
sudo pip install selenium datetime