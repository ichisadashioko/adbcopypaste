javac -source 1.7 -target 1.7 HelloWorld.java
"$ANDROID_SDK_ROOT"/build-tools/27.0.2/dx \
    --dex --output classes.dex HelloWorld.class

$ANDROID_SDK_ROOT/build-tools/30.0.3/dx --dex --output io.github.ichisadashioko.android.adbcopypaste.Copy.dex Copy.class


adb shell CLASSPATH=/data/local/tmp/classes.dex app_process / HelloWorld

javac -source 1.8 -target 1.8 Copy.java
$ANDROID_SDK_ROOT/build-tools/30.0.3/dx --dex --output Copy.dex Copy.class
adb shell rm /data/local/tmp/Copy.dex
adb push Copy.dex /data/local/tmp/
adb shell CLASSPATH=/data/local/tmp/Copy.dex app_process / Copy /data/local/tmp/utf8.txt
