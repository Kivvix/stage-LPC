#! /bin/bash

echo "objId,ra,dec,u" > $1/src-stack-$2-u.csv

for i in `ls $1/src-stack-$2-u*.csv`; do
	tail -n $(( $(wc -l $i | cut -d" " -f1) - 1 )) $i >> $1/src-stack-$2-u.csv
done

echo "objId,ra,dec,u" > $1/src-sdss-$2-u.csv

for i in `ls $1/src-sdss-$2-u*.csv`; do
	tail -n $(( $(wc -l $i | cut -d" " -f1) - 1 )) $i >> $1/src-sdss-$2-u.csv
done
