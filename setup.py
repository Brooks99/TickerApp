from setuptools import setup

APP = ['ticker.py']
DATA_FILES = ['config.json']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['yfinance', 'feedparser', 'pandas_market_calendars'],
    'plist': {
        'CFBundleName': 'Tickrly',
        'CFBundleDisplayName': 'Tickrly',
        'CFBundleIdentifier': 'com.tickrly.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)