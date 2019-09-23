#! /usr/bin/python
import sys, os
from distutils.core import setup
from glob import glob

# to install type: 
# python setup.py install --root=/

locales=map(lambda i: ('share/'+i,[''+i+'/othman.mo',]),glob('locale/*/LC_MESSAGES'))
data_files=[('share/othman/',glob('othman-data/*'))]
data_files.extend(locales)
setup (name='Othman', version='0.3.0',
      description='Othman Quran Browser',
      author='Muayyad Saleh Alsadi',
      author_email='alsadi@ojuba.org',
      url='http://othman.ojuba.org/',
      license='Waqf',
      packages=['othman'],
      scripts=['othman-browser'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          ],
      data_files=data_files
)


