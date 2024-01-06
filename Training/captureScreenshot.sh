#!/bin/bash

CAPT_DIR="$1"
ANDROID_SERIAL="$2"


#adb -s $ANDROID_SERIAL shell input keyevent 224 
#sleep 2s
adb -s $ANDROID_SERIAL shell -n screencap -p /sdcard/screen_exp.png
adb -s $ANDROID_SERIAL pull /sdcard/screen_exp.png $CAPT_DIR/screen_exp.png
adb -s $ANDROID_SERIAL shell -n rm /sdcard/screen_exp.png
