#!/bin/sh

set -e
set -x

APP="Add CMS1500 to Intergy"

rm -rf build/ dist/

python setup.py py2app

# Figure out what version we just built
VERSION=$(defaults read "$(pwd)/dist/$APP.app/Contents/Info.plist" CFBundleVersionString)

hdiutil create \
        -volname "$APP-$VERSION" \
        -srcfolder "dist/$APP.app/" \
        -ov -format UDZO \
        "dist/$APP-$VERSION.dmg"
