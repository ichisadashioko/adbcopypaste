# Building

Check [`compile.py`](compile.py)

# Example

```sh
adb push ../utf8_1 /data/local/tmp/
adb push ../utf8_2 /data/local/tmp/
adb push shellcopy.dex /data/local/tmp/

# copy content of utf8_1 to clipboard
adb shell CLASSPATH=/data/local/tmp/shellcopy.dex app_process / shellcopy.Copy /data/local/tmp/utf8_1
# focus on any EditText component and send paste event
adb shell input keyevent 279

# copy content of utf8_2 to clipboard
adb shell CLASSPATH=/data/local/tmp/shellcopy.dex app_process / shellcopy.Copy /data/local/tmp/utf8_2
# focus on any EditText component and send paste event
adb shell input keyevent 279
```
