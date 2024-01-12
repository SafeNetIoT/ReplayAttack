#!/bin/bash

MAC_DEVICE="$1"
INTERFACE="$2"
MAC_SMARTPHONE="$3"
SNIFF_TIME="$4"

filter="(ether src $MAC_DEVICE and ether dst $MAC_SMARTPHONE) or (ether src $MAC_SMARTPHONE and ether dst $MAC_DEVICE)"

   EXP_FOLDER="Result/$MAC_DEVICE/Experiments/Home/Experiment"
   mkdir -p "$EXP_FOLDER"
   
    tshark -i "$INTERFACE" -f "$filter" -w "$EXP_FOLDER/capture.pcap" -a duration:"$SNIFF_TIME" &
    
    echo "Start triggering the device"
   
   wait
   
   chmod +r "$EXP_FOLDER"/capture.pcap
   
   python3 TrainingReplay.py "$EXP_FOLDER/capture.pcap" "$EXP_FOLDER" $MAC_SMARTPHONE $MAC_DEVICE  > $EXP_FOLDER/accuracy.txt
   
   echo "TRAINING DONE"



