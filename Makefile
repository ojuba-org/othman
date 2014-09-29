DESTDIR?=/
datadir?=$(DESTDIR)/usr/share
INSTALL=install

SOURCES=$(wildcard *.desktop.in)
TARGETS=${SOURCES:.in=} othman-data/quran.db

all: $(TARGETS) icons othman-data/ix.db

icons:
	for i in 96 72 64 48 36 32 24 22 16; do \
		convert Othman-128.png -resize $${i}x$${i} Othman-$${i}.png; \
	done

othman-data/ix.db: othman-data/quran.db
	rm othman-data/ix.db || :
	python gen-index.py

othman-data/quran.db: othman-data/quran.sql othman-data/update-othmani.sql
	rm $@ || :
	cat $^ | sqlite3 $@

pos:
	make -C po all

install: all
	rm othman-data/quran-kareem.png || :
	python setup.py install -O2 --root $(DESTDIR)
	$(INSTALL) -d $(datadir)/applications/
	$(INSTALL) -m 0644 Othman.desktop $(datadir)/applications/
	for i in 96 72 64 48 36 32 24 22 16; do \
		install -d $(datadir)/icons/hicolor/$${i}x$${i}/apps; \
		$(INSTALL) -m 0644 -D Othman-$${i}.png $(datadir)/icons/hicolor/$${i}x$${i}/apps/Othman.png; \
	done

%.desktop: %.desktop.in pos
	intltool-merge -d po $< $@

clean:
	rm -f $(TARGETS) othman-data/ix.db
	for i in 96 72 64 48 36 32 24 22 16; do \
		rm -f Othman-$${i}.png; \
	done
