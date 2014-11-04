#! /bin/bash

echo "\begin{description}"
for i in `ls glossaire/`; do
	echo "\item[`head -n 1 glossaire/$i` :] `sed -n '2~1'p glossaire/$i`"
	echo "\vspace{5mm}"
done
echo "\end{description}"