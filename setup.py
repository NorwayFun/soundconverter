import sys
import DistUtilsExtra.auto

# using DistUtilsExtra.auto.setup instead of setup from distutils.core will automatically
# assuming the prefix is /usr:
# - compile and install po files to /usr/share/locale*.mo,
# - install .desktop files to /usr/share/applications
# - install all the py files to /usr/lib/python3.8/site-packages/soundconverter
# - copy bin to /usr/bin
DistUtilsExtra.auto.setup(
    name='soundconverter',
    version='3.0.2',
    description=(
        'A simple sound converter application for the GNOME environment. '
        'It writes WAV, FLAC, MP3, and Ogg Vorbis files.'
    ),
    license='GPL-3.0',
    data_files=[
        ('share/metainfo/', ['data/soundconverter.appdata.xml']),
        ('share/pixmaps/', ['data/soundconverter.png']),
        ('share/icons/hicolor/scalable/apps', ['data/soundconverter.svg']),
    ],
)
