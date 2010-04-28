
INSTALL=install

SOURCES=$(wildcard *.desktop.in)
TARGETS=${SOURCES:.in=}

all: $(TARGETS) othman-data/ix.db

othman-data/ix.db: othman-data/quran.db
	rm othman-data/ix.db || :
	python gen-index.py

pos:
	make -C po all

install: all
	python setup.py install -O2 --root $(DESTDIR)
	$(INSTALL) -d $(datadir)/applications/
	$(INSTALL) -m 0644 Othman.desktop $(datadir)/applications/

%.desktop: %.desktop.in pos
	intltool-merge -d po $< $@

clean:
	rm -f $(TARGETS)
