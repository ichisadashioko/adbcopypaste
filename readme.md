# `adbcopypaste`

Copy and paste text from your computer into Android phone via `adb` (Unicode character supports).

# Usage

## Preparation

- Install the apk - `adbcopypaste` application.
- Enable external storage read/write permission for `adbcopypaste`.

## Copying and Pasting

- Save text you want to copy in a text file in your computer. And it must be encoded in `UTF-8` encoding.
- Push the text to the device via `adb` to `/sdcard/utf8.txt`
- Run this shell command on the device (via `adb shell`) - `am startservice io.github.ichisadashioko.android.adbcopypaste/.CopyService`
- Focus on any pastable text widget.
- Send the paste key event (via `adb shell`) - `input keyevent 279`

# Note

The `MainActivity` must be running before we can start the service from shell (in Android 8.0+?).

```sh
am startservice io.github.ichisadashioko.android.adbcopypaste/.CopyService
```

# Grant WRITE_EXTERNAL_STORAGE permission from shell (not working in some devices)

```
pm grant io.github.ichisadashioko.android.adbcopypaste android.permission.WRITE_EXTERNAL_STORAGE
```

