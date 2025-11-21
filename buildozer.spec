[app]

# App title and package name
title = Gold Trading Pro
package.name = goldtradingapp
package.domain = org.goldtrading

# Source code - NO DUPLICATES
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

# Main entry point - ONLY APPEARS ONCE
source.main = main_complete.py

# Version
version = 1.0

# Requirements - MOBILE-FRIENDLY ONLY (NO pandas, NO numpy)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,pillow

# Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Orientation
orientation = portrait

# Supported architectures
android.archs = arm64-v8a, armeabi-v7a

# Android API level
android.api = 31
android.minapi = 21
android.ndk = 25b

# Enable AndroidX support
android.enable_androidx = True

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Build warnings
warn_on_root = 1

# Build directory
build_dir = ./.buildozer

# Binary directory
bin_dir = ./bin
