#!/bin/bash
ANDROID_SERIAL="$1"
MAC_DEVICE="$2"
INTERFACE="$3"
PACKAGE="$4"

CROP_FUN=$(cat Result/$MAC_DEVICE/Capture/Fun_crop.txt)
CROP_REVERSE=$(cat Result/$MAC_DEVICE/Capture/Reverse_crop.txt)

tap_time="5s"
open_time="10s"

sniffing_time=60



#temp=$(./switch_network.sh $ANDROID_SERIAL $INTERFACE)
#MAC_SMARTPHONE="${temp##*$'\n'}"
MAC_SMARTPHONE=$5


#temp_target_ip_address=$(arp -a | grep $MAC_DEVICE | awk '{print $2}')
#let len=${#temp_target_ip_address}-1
#IP_DEVICE=$(cut -c 2-$len <<< $temp_target_ip_address)
#iptables -I FORWARD 1 -i $INTERFACE -o eth1 -m mac --mac-source $MAC_DEVICE -j DROP
#iptables -I FORWARD 2 -i eth1 -o $INTERFACE -j DROP -d $IP_DEVICE
#trap 'iptables -D FORWARD -i $INTERFACE -o eth1 -m mac --mac-source $MAC_DEVICE -j DROP; iptables -D  FORWARD -i eth1 -o $INTERFACE -j DROP -d $IP_DEVICE' SIGINT


filter="(ether src  $MAC_DEVICE and ether dst $MAC_SMARTPHONE) or (ether dst $MAC_DEVICE and ether src $MAC_SMARTPHONE)"
#filter="(ether src  $MAC_DEVICE or ether dst $MAC_DEVICE)"


EXP_FOLDER="Result/$MAC_DEVICE/Experiments/LocalConnectivity"
mkdir -p $EXP_FOLDER

adb -s $ANDROID_SERIAL shell input keyevent 224
sleep 2s


tshark -i "$INTERFACE" -f "$filter" -w "$EXP_FOLDER/capture.pcap" -a duration:"$sniffing_time" &

./trigger_functionality_testing.sh $ANDROID_SERIAL $PACKAGE Result/$MAC_DEVICE/Capture $CROP_FUN Result/$MAC_DEVICE/Fun_coordinates.txt Fun True $tap_time $open_time

mv Result/$MAC_DEVICE/Capture/screen_exp.png Result/$MAC_DEVICE/Capture/Fun_reference.png
chmod +r  Result/$MAC_DEVICE/Capture/Fun_reference.png

./trigger_functionality_testing.sh $ANDROID_SERIAL $PACKAGE Result/$MAC_DEVICE/Capture $CROP_REVERSE Result/$MAC_DEVICE/Reverse_coordinates.txt Reverse True $tap_time $open_time

mv Result/$MAC_DEVICE/Capture/screen_exp.png Result/$MAC_DEVICE/Capture/Reverse_reference.png
chmod +r  Result/$MAC_DEVICE/Capture/Reverse_reference.png
 wait

#python3 CheckLocalConnectivity.py "$EXP_FOLDER/capture.pcap"

chmod +r  $EXP_FOLDER/capture.pcap

#iptables -D FORWARD -i $INTERFACE -o eth1 -m mac --mac-source $MAC_DEVICE -j DROP
#iptables -D  FORWARD -i eth1 -o $INTERFACE -j DROP -d $IP_DEVICE
