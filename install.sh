#!/usr/bin/env bash

PATH_LOCAL="/opt/scripts"
PATH_LINK="/usr/local/bin"

check() {
[ ! -x "$(which python3)" ] && {
    echo "python is not installed, please install it."
    exit 1
}

if [ $(id -u) != 0 ]; then
    echo "permission denied, try again using sudo"
    exit 1
fi
}

banner() {
echo "Installing..."
}

prepare() {
if [ ! -e $PATH_LOCAL ]; then sudo mkdir $PATH_LOCAL; fi
if [ ! -e $PATH_LOCAL/certscan ]; then return; fi
}

install(){
command -v pip > /dev/null 2>&1 && {
    pip install -r requirements.txt > /dev/null 2>&1
}
command -v pip3 > /dev/null 2>&1 && {
    pip3 install -r requirements.txt > /dev/null 2>&1
}
sudo cp -r ../certscan $PATH_LOCAL/
}

link(){
sudo ln -sf $PATH_LOCAL/certscan/certscan.py $PATH_LINK/certscan
sudo chmod +x $PATH_LOCAL/certscan/certscan.py
sudo chmod +x $PATH_LINK/certscan
}

main(){
check
banner
echo -ne '>>>>>>>>>                          [20%]\r'
sleep 0.5
echo -ne '>>>>>>>>>>>>>>>>                   [40%]\r'
prepare
sleep 0.5
echo -ne '>>>>>>>>>>>>>>>>>>>>>>>            [60%]\r'
install
sleep 0.5
echo -ne '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      [80%]\r'
link
sleep 0.5
echo -ne '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[100%]\r'
echo -ne '\n'
echo -e "\certscan was installed in: $PATH_LOCAL"
}

main