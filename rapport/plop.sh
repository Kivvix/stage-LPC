#! /bin/bash

cd $HOME/Documents/Rapport
make
#evince main.pdf &
zenity --question --text="Compile moi !" && gnome-terminal gnome-terminal --window-with-profile=LaTeX -e "./$0"
