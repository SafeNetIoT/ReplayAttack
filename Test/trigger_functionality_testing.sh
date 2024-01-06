#!/bin/bash

PHONE="smartphoneGoogle"
CAPT_DIR="$3"

function waitphone {
    while [ -z "$PHONE_FOUND" ]; do
        echo "Phone not found, waiting for $PHONE/$ANDROID_SERIAL"
        sleep 5
       PHONE_FOUND=`adb devices | grep $ANDROID_SERIAL`
    done
}

ANDROID_SERIAL="$1"
echo Phone is: $PHONE/$ANDROID_SERIAL
PHONE_FOUND=`adb devices | grep $ANDROID_SERIAL | grep device`
waitphone
echo Phone ready, proceeding...

package="$2"
crop="$4"
file_path="$5"

name="$6"

screen="$7"

tap_time="$8"

open_time="$9"


echo "Starting Functionality"


waitphone
adb -s $ANDROID_SERIAL shell -n monkey -p $package -c android.intent.category.LAUNCHER 1 &>/dev/null

sleep $open_time

while read -r function
do
waitphone
adb -s $ANDROID_SERIAL shell -n input $function
sleep $tap_time
done < "$file_path"

waitphone
adb -s $ANDROID_SERIAL shell -n input tap 1010 2190
sleep 1s

 
if [[ $screen = "True" ]]
then 
 #capture screenshot
./captureScreenshot.sh $CAPT_DIR $ANDROID_SERIAL
 #comparing screenshot
COMP=$(convert $CAPT_DIR/${name}_reference.png $CAPT_DIR/screen_exp.png -crop $crop +repage miff:- | compare -verbose -metric MAE  - $CAPT_DIR/result.png 2>&1 | grep all | awk '{print $2}')
  if [ $COMP = "0" ]; then
       echo "Comparison ok"
  else
  echo "Error comparison"      
  fi
fi
waitphone
adb -s $ANDROID_SERIAL shell am force-stop $package


