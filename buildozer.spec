[app]
title = Mi
package.name = mi
package.domain = com.mi.connect
source.dir =.
source.include_exts = py,png,jpg,kv,json
version = 3.0
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,pillow,urllib3,plyer,jnius
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png
[buildozer]
log_level = 2
[app:android]
permissions = INTERNET,CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATION,VIBRATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True
android.ant = auto
p4a.bootstrap = sdl2