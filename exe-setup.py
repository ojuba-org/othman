#! /usr/bin/python
import sys, os
from distutils.core import setup
from glob import glob

import py2exe

# to create exe type:
# python exe-setup.py py2exe -O2

# NOTE: before you use this tool you should run make to generate index and locale files


locales=map(lambda i: ('locale/' + i, ['' + i + '/othman.mo',]), glob('locale/*/LC_MESSAGES'))
data_files=[('othman-data',
             glob('othman-data/*')),
             ('.',
              ['COPYING'] + glob('LICENSE*') + glob('README*'))]
data_files.extend(locales)

setup (name='Othman', version='0.2.0',
    description='Othman Quran Browser',
    author='Muayyad Saleh Alsadi',
    author_email='alsadi@ojuba.org',
    url='http://othman.ojuba.org/',
    license='Waqf',
    packages=['othman'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        ],

    windows = [
                {
                      'script': 'othman-browser',
                      'icon_resources': [(1, "othman.ico")],
                }
            ],

    options = {
              'py2exe': {
                  'packages':'encodings',
                  'includes': 'cairo, pango, pangocairo, atk, gobject, gio',
              }
          },
    data_files=data_files
    )


