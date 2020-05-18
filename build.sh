#!/bin/sh

set -e
set -x

APP="Add CMS1500 to Intergy"

rm -rf build/ dist/

python setup.py py2app

hdiutil create -volname "$APP" -srcfolder "dist/$APP.app/" -ov -format UDZO "dist/$APP.dmg"
