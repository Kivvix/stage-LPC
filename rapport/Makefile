SRC = main
#REP= ./sources_gnuplot

DEBUG_MODE ?= N
LATEX = pdflatex --shell-escape

ifeq ($(DEBUG_MODE), Y)
#LATEX += -interaction=nonstopmode
else
LATEX +=  -interaction=batchmode
endif

BIBTEX = bibtex -terse
RERUN = ‘(There were undefined references|Rerun to get (cross-references|the bars) right)’
UNDEFINED = ‘((Reference|Citation).*undefined)|(Label.*multiply defined)’

.PHONY:all $(REP)

#all: $(REP) ${SRC}.pdf
all: complet

$(REP):
	@$(MAKE) -C $@ $(MAKECMDGOALS)

propre: $(REP)
	@echo “suppression des fichiers de compilation”
	@# fichiers de compilation latex
	@rm -f *.log *.aux *.dvi *.toc *.lot *.lof
	@# fichiers de bibtex
	@rm -f *.bbl *.blg

DEB=$(shell date -d now +%s)

complet:
	@echo -e "\033[1mCompilation complète\033[0m"
	@date +%H:%M:%S
	@notify-send --expire-time=27000 -i /usr/share/icons/gnome/32x32/emblems/emblem-new.png "Début de compilation" "À : $$(date +%H:%M:%S)"
	@echo -e "\033[1m\t Compilation n°1\033[0m"
	@${LATEX} ${SRC}
	@date +%H:%M:%S
	@notify-send -i /usr/share/icons/gnome/32x32/emblems/emblem-default.png "Compilation n°1" "Check : $$(date +%H:%M:%S)"
	@if [ -e ${SRC}.bbl ]; then echo -e "\033[1m\t Bibliographie\033[0m"; ${BIBTEX} ${SRC} ; notify-send -i /usr/share/icons/gnome/32x32/emblems/emblem-documents.png "Bibliographie" "Check : $$(date +%H:%M:%S)"; fi
	@echo -e "\033[1m\t Compilation n°2\033[0m"
	@${LATEX} ${SRC}
	@date +%H:%M:%S
	@notify-send -i /usr/share/icons/gnome/32x32/emblems/emblem-default.png "Compilation n°2" "Check : $$(date +%H:%M:%S)"
	@echo -e "\033[1m\t Compilation n°3\033[0m"
	@${LATEX} ${SRC}
	@date +%H:%M:%S
	@notify-send -i /usr/share/icons/gnome/32x32/emblems/emblem-generic.png "Compilation n°3" "Check : $$(date +%H:%M:%S)"
	@echo Temps de compilation : $$(( $$(date -d now +%s) - $(DEB) )) s
	@notify-send -i /usr/share/icons/gnome/32x32/actions/document-open-recent.png "Temps de compilation" "$$(( $$(date -d now +%s) - $(DEB) )) s"

initial: propre
	@echo „suppression des fichiers cibles“
	@rm -f ${SRC}.ps ${SRC}.pdf

bib:
	bibtex ${SRC}

%.pdf : %.tex
	@echo „compilation du tex“
	${LATEX} $<
	@if [ -e ${SRC}.bbl ]; then ${BIBTEX} $* ; fi
	@if egrep -q $(RERUN) $*.log ; then echo «passe LaTeX» \
	&& $(LATEX) $<; fi
	@if egrep -q $(RERUN) $*.log ; then echo «passe LaTeX» \
	&& $(LATEX) $<; fi
	@echo “Citations ou références indéfinies:»
	@egrep -i $(UNDEFINED) $*.log || echo «Aucune»
