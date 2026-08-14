[app]
title = Tower Dominion
package.name = towerdominion
package.domain = org.tower.game
source.dir =.
version = 0.1
requirements = python3,pygame,android
orientation = landscape

[buildozer]
log_level = 2

[app:android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True
