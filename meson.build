project('othman',
          version: '2.0',
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

document_files = ['README.md', 'README-ar.txt']
install_data(
    document_files,
    install_dir : join_paths(get_option('datadir'),'doc/othman')
)

licenses_files = ['LICENSE-en' , 'LICENSE-ar.txt','COPYING']
install_data(
    document_files,
    install_dir : join_paths(get_option('datadir'),'licenses/othman')
)

message('create icons...')
run_command('mkdir','-p','icons',check:true)
foreach size : ['16', '22', '24', '32', '36', '48', '64', '72', '96', '128', '256', '512' ]
  run_command('convert','Othman-128.png','-resize',('@0@x@1@').format(size,size),('icons/othman-@0@.png').format(size),check:true)
endforeach

message('create ix.db...')
python_exe = find_program('python3', 'python')
run_command(python_exe,'gen-index.py',check:true)

data_files = [
              ['icons/hicolor/16x16/apps', ['icons/othman-16.png'],['Othman.png']],
              ['icons/hicolor/22x22/apps', ['icons/othman-22.png'],['Othman.png']],
              ['icons/hicolor/24x24/apps', ['icons/othman-24.png'],['Othman.png']],
              ['icons/hicolor/32x32/apps', ['icons/othman-36.png'],['Othman.png']],
              ['icons/hicolor/36x36/apps', ['icons/othman-48.png'],['Othman.png']],
              ['icons/hicolor/48x48/apps', ['icons/othman-64.png'],['Othman.png']],
              ['icons/hicolor/64x64/apps', ['icons/othman-72.png'],['Othman.png']],
              ['icons/hicolor/72x72/apps', ['icons/othman-96.png'],['Othman.png']],
              ['icons/hicolor/96x96/apps', ['icons/othman-128.png'],['Othman.png']],
              ['icons/hicolor/128x128/apps',['icons/othman-256.png'],['Othman.png']],
              ['icons/hicolor/256x256/apps',['icons/othman-512.png'],['Othman.png']],
              ['icons/hicolor/512x512/apps',['icons/othman-16.png'],['Othman.png']],
              ['icons/hicolor/scalable/apps',['othman-data/quran-kareem.svg'],['Othman.svg']],
              ['pixmaps',['icons/othman-128.png'],['Othman.png']],
              ['othman',['othman-data/ix.db'],['ix.db']],
              ['othman',['othman-data/quran.db'],['quran.db']],
              ['othman',['othman-data/quran-kareem.svg'],['quran-kareem.svg']]
              ]
              
foreach files_ : data_files
  foreach i : files_[1]
    install_data(
      i,
      install_dir : join_paths(get_option('datadir'),files_[0]),
      rename      : files_[2]
  )
  endforeach
endforeach

python = import('python')
py_sources = [
    'othman/core.py',
    'othman/gtkUi.py',
    'othman/__init__.py',
    'othman/univaruints.py'
]
python.find_installation('python3').install_sources(py_sources,
  subdir: 'othman',
)

install_data(
    'othman-browser',
    install_mode: 'rwxr-xr-x',
    install_dir : get_option('bindir')
)

i18n = import('i18n')
desktop_file = i18n.merge_file(
        input: 'Othman.desktop.in',
       output: 'othman.desktop',
         type: 'desktop',
       po_dir: 'po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)
  
subdir('po')

