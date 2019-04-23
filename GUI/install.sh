#!/bin/bash - 
#===============================================================================
#
#          FILE: install.sh
# 
#         USAGE: ./install.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 24/4/19 00:42
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
mkdir /usr/share/PyChat
path=/usr/share/PyChat
cp -r ./styles $path/styles
cp -r ./TCP $path/TCP
cp -r ./var $path/var

cp Model.py $path/Model.py
cp View.py $path/View.py
cp codes.py $path/codes.py
cp PyChat.py $path/PyChat.py
cp server.py $path/server.py

ln -s $path/PyChat.py /usr/bin/pychat

chmod +x $path/PyChat.py
chmod +x /usr/bin/pychat


