[app]
title = Gold Trading Pro
package.name = goldtradingapp
package.domain = org.goldtrading
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
source.main = main.py
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,pillow
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK
android.archs = armeabi-v7a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.enable_androidx = True
android.accept_sdk_license = True
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 0
android.accept_sdk_license = True
