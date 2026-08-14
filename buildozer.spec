[app]
title = Tower Dominion
package.name = towerdominion
package.domain = org.tower.game
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,pygame
orientation = landscape
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

[app:android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.arch = armeabi-v7a
p4a.bootstrap = sdl2
p4a.branch = master
p4a.fork = kivy
android.accept_sdk_license_agreement = True
android.permissions = INTERNET
