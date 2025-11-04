# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ticker.py'],
    pathex=[],
    binaries=[],
    datas=[('config.json', '.'), ('assets/Tickrly.icns', 'assets'), ('LICENSE', '.')],  # Include config.json, icon, and license in the bundle
    hiddenimports=[
        'yfinance',
        'feedparser',
        'pandas_market_calendars',
        'tkinter',
        'tkinter.ttk',
        '_tkinter',
        'logging',
        'locale',
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Tickrly',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/Tickrly.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Tickrly',
)

app = BUNDLE(
    coll,
    name='Tickrly.app',
    icon='assets/Tickrly.icns',
    bundle_identifier='com.tickrly.app',
    info_plist={
        'LSEnvironment': {
            'LANG': 'en_US.UTF-8',
            'LC_ALL': 'en_US.UTF-8',
        },
        'CFBundleName': 'Tickrly',
        'CFBundleDisplayName': 'Tickrly',
        'CFBundleExecutable': 'Tickrly',
        'CFBundlePackageType': 'APPL',
    'CFBundleShortVersionString': '1.0.2',
        'NSHighResolutionCapable': True,
    },
)