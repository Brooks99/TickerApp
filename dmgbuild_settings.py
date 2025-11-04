import os

# dmgbuild settings for Tickrly
# Uses assets/Tickrly.icns created earlier and places the app on the left
# with a link to /Applications on the right. Adjust coordinates if you want
# a different layout.

PROJECT_ROOT = os.getcwd()
ICONS_DIR = os.path.join(PROJECT_ROOT, "assets")
ICON_PATH = os.path.join(ICONS_DIR, "Tickrly.icns")

settings = {
    # DMG appearance
    'volume_name': 'Tickrly',
    'format': 'UDZO',  # compressed image
    'compression_level': 9,

    # Use our app icon as the volume icon
    'volume_icon': ICON_PATH,

    # Window configuration: size (width, height)
    'window_size': (640, 320),

    # Background can be an image path (PNG) or None for default
    'background': None,

    # Icon locations inside the DMG window (x, y) coordinates
    # Coordinates chosen for a pleasant centered layout on 640x320
    'icon_locations': {
        'Tickrly.app': (140, 120),
        'Applications': (460, 120),
        'LICENSE': (300, 220),  # Position the license file below the apps
    },

    # Files to include in the DMG
    'files': ['dist/Tickrly.app', 'LICENSE'],

    # Shortcut to Applications folder
    'symlinks': {'Applications': '/Applications'},

    # Icon sizing in Finder view
    'icon_size': 128,
    'text_size': 14,

    # Misc
    'show_status_bar': False,
    'show_tab_view': False,
}

if __name__ == '__main__':
    print('This file is a settings module for dmgbuild. It is not meant to be executed.')
# -*- coding: utf-8 -*-
import os.path

# Use the same name for the volume as for the app
app = 'dist/Tickrly.app'
volname = 'Tickrly'
format = 'UDBZ'
size = '100M'

# Files to include
files = [app]

# Symlinks to create
symlinks = {'Applications': '/Applications'}

# Where to put things
icon_locations = {
    os.path.basename(app): (140, 120),
    'Applications': (500, 120)
}

# Window configuration
window = {
    'position': (100, 100),
    'size': (640, 280)
}
icon_size = 128