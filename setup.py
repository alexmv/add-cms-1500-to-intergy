from setuptools import setup

VERSION = "0.7.1"

APP = ["Add CMS1500 to Intergy.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "resources": "CMS-1500.pdf",
    "plist": {
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersionString": VERSION,
        "CFBundleIdentifier": "org.pythonmac.AddCMS1500toIntergy",
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
