[app]

# App title and package name
title = Gold Trading Pro
package.name = goldtradingapp
package.domain = org.goldtrading

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

# Main entry point
source.main = main.py

# Version
version = 1.0

# Requirements - REMOVED pandas/numpy (don't work on Android)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,pillow

# Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK

# Orientation
orientation = portrait

# Architecture - SINGLE ARCH for faster build
android.archs = armeabi-v7a

# Android API level
android.api = 31
android.minapi = 21
android.ndk = 25b

# Enable AndroidX support
android.enable_androidx = True
android.accept_sdk_license = True

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Build warnings
warn_on_root = 0

# Build directory
build_dir = ./.buildozer

# Binary directory
bin_dir = ./bin
