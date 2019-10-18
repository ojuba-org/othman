DESTDIR?=/
PREFIX?=$(DESTDIR)/usr
datadir?=$(PREFIX)/share
INSTALL=install
PYTHON=/usr/bin/python3
SOURCES=$(wildcard *.desktop.in)
TARGETS=${SOURCES:.in=}
TEST_DEPS=0

all: $(TARGETS) icons

icons:
	install -d icons; 
	for i in 96 72 64 48 36 32 24 22 16; do \
		convert Othman-128.png -resize $${i}x$${i} icons/Othman-$${i}.png; \
	done

othman-data/ix.db: othman-data/quran.db
	rm othman-data/ix.db || :
	$(PYTHON) gen-index.py

pos:
	make -C po all

install: all
	[ $(TEST_DEPS) == "1" ] && $(PYTHON) -c 'import gi; gi.require_version("Gtk", "3.0")'
	rm othman-data/quran-kareem.png || :
	$(PYTHON) setup.py install --prefix=$(PREFIX)
	$(INSTALL) -d $(datadir)/applications/
	$(INSTALL) -m 0644 Othman.desktop $(datadir)/applications/
	for i in 96 72 64 48 36 32 24 22 16; do \
		install -d $(datadir)/icons/hicolor/$${i}x$${i}/apps; \
		$(INSTALL) -m 0644 -D icons/Othman-$${i}.png $(datadir)/icons/hicolor/$${i}x$${i}/apps/Othman.png; \
	done

%.desktop: %.desktop.in pos
	echo "updating .desktop"
	intltool-merge -d po $< $@

clean:
	rm -f othman-data/ix.db

