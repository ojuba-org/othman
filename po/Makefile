POTFILE=$(shell cat POTFILES.in)
SOURCES=$(addprefix ../, $(POTFILE))
POFILES=$(wildcard *.po)
MOFILES=$(patsubst %.po,%.mo,$(POFILES))
all: $(MOFILES)

othman.pot: $(SOURCES)
	intltool-update -g othman -p

%.mo: %.po
	msgfmt $*.po -o $*.mo
	mkdir -p ../locale/$*/LC_MESSAGES/ || :
	cp $*.mo ../locale/$*/LC_MESSAGES/othman.mo
	touch ../*.desktop.in

%.po: othman.pot
	intltool-update -g othman -d $*

