POTFILE=$(shell cat POTFILES.in)
SOURCES=$(addprefix ../, $(POTFILE))

all: $(wildcard *.po)

othman.pot: $(SOURCES)
	intltool-update -g othman -p

%.po: othman.pot
	intltool-update -g othman -d $*
	mkdir -p ../locale/$*/LC_MESSAGES/ || :
	msgfmt $*.po -o ../locale/$*/LC_MESSAGES/othman.mo


