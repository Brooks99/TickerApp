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