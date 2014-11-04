compareSrc
==========

> *Analyse des produits du logiciel de traitement d'images de LSST*


L'analyse des produit du logiciel de traitement d'images de LSST (`Stack`) s'effectue par une comparaison avec une base de données pré-existante, celle générée par les observations de SDSS sur la *stripe 82*. Cela s'effectue à l'aide du module `compareSrc`, divisé en trois sous-module :
* `data` : qui conserne la recherche et la sauvegarde des données utiles ;
* `cmp` : le cœur de l'analyse puisqu'il s'agit de l'association des sources SDSS avec une source LSST ;
* `stat` : qui conserne l'étude statistique des résultats de la comparaison.


Module `data`
-------------

Le module `data` est entièrement écrit en *Python* et gère la recherche des données utiles à la comparaison des bases de données. Pour cela il sauvegarde un `id`, les coordonnées (sous la forme `RA`, `Dec` pour ascension droite et déclinaison) et la magnitude dans un filtre (il existe 5 filtres `u`, `g`, `r`, `i`, `z` correspondant chacun à une longueur d'onde particulière) des sources SDSS et LSST.

Les données de SDSS sont stockées dans une base de données accessible depuis le Web, une requête *SQL* est donc effectuée pour récupérer les données intéressantes.

Les données de LSST sont stockées sous la forme de fichiers `fits` dans une table binaire, par contre la magnitude présente est une magnitude relative aux conditions de la prise de vu, et il est donc nécessaire de calibrer cette valeur à l'aide d'une constante, `fluxMag0`, propre au fichier et récupérée dans une base de données.

Module `cmp`
------------

Le module `cmp` est entièrement écrit en *C++* et permet l'association d'une source SDSS à une source LSST. L'écart entre les deux sources est en suite calculer puis comparer à l'aide du module `stat`.

Différentes méthodes d'association sont envisageable, celle implémenté est une méthode qui fonctionne à l'aide d'un voisinage constant de *2 arcsec*.

Module `stat`
-------------

Le module `stat` est lui aussi entièrement écrit en *C++* et utilise le *framework* `ROOT` pour la représentation graphique des données.

Ce module lit les fichiers `csv` généré par le module `cmp` et en produit une série d'histogrammes représentant l'erreur moyenne commise à l'aide de la densité de delta de coordonnées et de magnitudes.

Script `init.py`
----------------

Pour une utilisation plus simple et sûre, les différents modules sont lancés à partir du script `init.py`. Celui-ci génère les fichiers de configuration des deux modules *C++* et les compile.
Il crée un fichier `job.py` indiquant les modules qui seront appelés.
Il lance à l'aide du programme `qsub` le job `job.csh` script écrit en *C-shell* appelant le fichier `job.py`.

Ainsi le choix ainsi que l'ordre des instructions peu être personnalisable au lancement du script `init.py`.
