[app]
title = Tower Dominion
package.name = towerdominion
package.domain = org.tower.game
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,pygame==2.5.2,sdl2,sdl2_image,sdl2_mixer,sdl2_ttf,android
orientation = landscape
fullscreen = 0

[buildozer]
log_level = 1

[app:android]
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license_agreement = True
android.ant_options = -Xmx4096m
p4a.url = https://github.com/kivy/python-for-android.git
p4a.branch = master
p4a.fork = kivy
Hide side panel
