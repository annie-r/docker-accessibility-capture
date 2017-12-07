#!/bin/bash
#echo $PATH

while :
do
  a=1
done

ip=$(ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}')
socat tcp-listen:$ANDROID_EMULATOR_PORT,bind=$ip,fork tcp:127.0.0.1:$ANDROID_EMULATOR_PORT &
socat tcp-listen:$ADB_PORT,bind=$ip,fork tcp:127.0.0.1:$ADB_PORT &

/opt/android-sdk-linux/emulator/emulator64-arm -avd "docker-accessibility-capture" \
                  -port $ANDROID_EMULATOR_PORT \
                  -no-boot-anim \
                  -no-window \
                  -no-audio \
                  -gpu swiftshader \
				  -verbose \ &

                  #-no-snapshot-save \
				  #-qemu -usbdevice tablet -vnc :0

#adb wait-for-device
echo "Waiting for emulator to start..." 

bootanim=""
failcounter=0
counter=0
until [[ "$bootanim" =~ "stopped" ]]; do
   
   bootanim=`adb -e shell getprop init.svc.bootanim 2>&1`
   if [[ "$bootanim" =~ "not found" ]]; then
      let "failcounter += 1"
      if [[ $failcounter -gt 3 ]]; then
        echo "  Failed to start emulator" 
        exit 1
      fi
   fi
   #if [[ $(($counter % 10)) -eq 0 ]]; then
      #adb shell screencap -p | perl -pe 's/\x0D\x0A/\x0A/g' > ./logs/screen$counter.png
   #fi
   let "counter +=1"
   echo "waiting $counter"
   sleep 1
done
adb devices
adb logcat

adb install app.apk
adb shell input keyevent 82
adb shell monkey -p "+app_info['package']+" -c android.intent.category.LAUNCHER 1
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png /data/screen.png

