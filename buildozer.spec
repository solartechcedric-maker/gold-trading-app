[app]
title = GoldTradingPro
package.name = goldtradingpro
package.domain = org.goldtrading
source.dir = .
source.include_exts = py
version = 0.1

# USE MOST STABLE VERSIONS
requirements = python3,kivy==2.1.0

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

# PROVEN STABLE API LEVELS
android.api = 27
android.minapi = 21
android.ndk = 19c
android.accept_sdk_license = True
android.archs = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
