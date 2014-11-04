PROJET=stat
EDITOR=geany
README=
INPUT_DATA= all



ROOTSYST= /usr/local/root/v5.34.18
CC=g++
CFLAGS=  -I$(ROOTSYST)/include -g -pg
#LDFLAGS= -L$(ROOTSYST)/lib -lCore -lCint -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lTree -lRint -lPostscript -lMatrix -lPhysics -lz -lGui -pthread -lm -ldl -rdynamic -lThread -lMathCore
LDFLAGS= $(shell root-config --cflags --libs)
SRC= $(wildcard *.cpp)
OBJ= $(SRC:.cpp=.o)

all: $(PROJET)

$(PROJET):
	g++ $(CFLAGS) -c $(SRC) && libtool --mode=link g++  -g -o $(PROJET) $(OBJ) $(LDFLAGS)

.PHONY: clean zip mrpropre val 
clean :
	rm -f $(OBJ) *~ core

mrpropre : clean
	rm -f $(PROJET) $(OBJ) *~

zip: mrpropre
	@tar -zcvf ../$(PROJET).tar.gz *.cpp *.hpp Makefile $(README)

val :
	valgrind --leak-check=yes ./$(PROJET) $(INPUT_DATA)

open :
	$(EDITOR) $(SRC) $(wildcard *.hpp) &
