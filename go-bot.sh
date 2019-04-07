#!/data/data/com.termux/files/usr bash
pkg install ruby figlet-y
gems install lolcat
pip2 install mechanize && pip install requests

clear
clear
sleep 1
echo "\033[96m silahkan Pm Author untuk membukanya :v"
python eaa.py
echo "\033[93m"
echo "#######################################################"
echo "# Author : r00t@star                                  #"
echo "# Team   : Sunda Cyber Army                           #"
echo "# Date   : 07 - 04 - 2019                             #"
echo "# facebook : https://www.facebook.com/BintangAlifff   #"
echo "# InstaGram : @bintang_alif16                         #"
echo "#######################################################"
sleep 2
echo ""
echo "\033[91m**************************************************************"
echo "\033[91m*\033[95m[1] \033[92mAuto_follow InstaGram.         \033[91m *"
echo "\033[91m*\033[95m[2] \033[92mAuto_liker InstaGram.          \033[91m *"
echo "\033[91m*\033[95m[00] \033[92mExiting The Program.          \033[91m *"
echo "\033[91m**************************************************************"
echo "\033[00m"
read -p "input choise -: " cl4; 
echo ""
if [ $cl4 = 1 ] || [ $cl4 = 1 ]
then
pkg install ruby-ri
ri auto_follow.rb
fi
