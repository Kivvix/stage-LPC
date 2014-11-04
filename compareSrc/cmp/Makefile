PROJET=cmp
EDITOR=geany
README=
INPUT_DATA=

CC=g++
CFLAGS=  -I /usr/lib64/boost -g -pg -Wall -Wextra
LDFLAGS= 
SRC= $(wildcard *.cpp) $(wildcard src/*.cpp)
OBJ= $(SRC:.cpp=.o)

all:$(PROJET)

%.o : %.cpp %.hpp
	$(CC) -c $< $(CFLAGS)

main.o : *.hpp

$(PROJET) : $(OBJ)
	$(CC) $(LDFLAGS) $+ -o $@

.PHONY: clean zip mrpropre val open cafe help
clean :
	rm -f $(OBJ) *~ core

mrpropre : clean
	rm -f $(PROJET) $(OBJ) *~

zip: mrpopre
	@tar -zcvf ../$(PROJET).tar.gz *.cpp *.hpp src/ Makefile $(README)

val :
	valgrind --leak-check=yes ./$(PROJET) $(INPUT_DATA)

open :
	$(EDITOR) $(SRC) $(wildcard *.hpp) &

cafe :
	@ echo "Je ne fais quand même pas le café !\n"

help :
	@ echo -e "\n ═══ Projet $(PROJET) ══════════════════\n option du Makefile :\n	- clean    : nettoie les fichiers objets\n	- mrpropre : nettoie les fichiers objets l'exécutable\n	- zip      : crée une archive .tar.gz du projet\n	- val      : execute valgrind\n	- open     : ouvre tous les fichiers avec $(EDITOR) (variable EDITOR)"

