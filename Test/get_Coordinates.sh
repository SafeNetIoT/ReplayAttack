#!/bin/bash

PHONE="smartphoneGoogle"

function waitphone {
    while [ -z "$PHONE_FOUND" ]; do
        echo "Phone not found, waiting for $PHONE/$ANDROID_SERIAL"
        sleep 5
       PHONE_FOUND=`adb devices | grep $ANDROID_SERIAL`
    done
}

ANDROID_SERIAL="954AY0U0EE"
echo Phone is: $PHONE/$ANDROID_SERIAL
PHONE_FOUND=`adb devices | grep $ANDROID_SERIAL | grep device`
waitphone
echo Phone ready, proceeding...

mac_device="$1"
name="$2"

trap 'python3 get_Coordinates.py $mac_device $name; rm Result/$mac_device/raw_${name}_coordinates.txt' SIGINT

adb -s $ANDROID_SERIAL shell getevent -l > Result/$mac_device/raw_${name}_coordinates.txt

if [ "$name" = "Fun" ]; then
    cp Result/$mac_device/Fun_coordinates.txt Result/$mac_device/Reverse_coordinates.txt
    cp Result/$mac_device/Fun_coordinates.txt Result/$mac_device/Ground_coordinates.txt
    sed '$ d' Result/$mac_device/Fun_coordinates.txt > Result/$mac_device/Ground_coordinates.txt
fi


