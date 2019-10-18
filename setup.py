#! /usr/bin/python
import sys, os
from distutils.core import setup
from glob import glob

from othman import __version__

# to install type: 
# python setup.py install --root=/

from distutils.command.build import build
from distutils.command.clean import clean

class my_build(build):
  def run(self):
    build.run(self)
    # generate data
    from othman.core import othmanCore, searchIndexer

    if not os.path.isfile('othman-data/ix.db'):
      q=othmanCore(False)
      ix=searchIndexer(True)
      for n,(o,i) in enumerate(q.getAyatIter(1, 6236)):
        for w in i.split(): ix.addWord(w,n+1)
      d=os.path.dirname(sys.argv[0])
      ix.save()

class my_clean(clean):
  def run(self):
    clean.run(self)
    try: os.unlink('othman-data/ix.db')
    except OSError: pass

locales=map(lambda i: ('share/'+i,[''+i+'/othman.mo',]),glob('locale/*/LC_MESSAGES'))
data_files=[('share/othman/',glob('othman-data/*'))]
data_files.extend(locales)
setup (name='Othman', version=__version__,
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
      cmdclass={'build': my_build, 'clean': my_clean},
      data_files=data_files
)

