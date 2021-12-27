rm -rf build dist
python3 setup.py py2app
rm -rf /Applications/WorkTimer.app
mv dist/WorkTimer.app /Applications
