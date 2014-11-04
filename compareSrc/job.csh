#! /usr/local/bin/csh

set runs=`ls /sps/lsst/data/dev/lsstprod/DC_2013_one_percent/calexp_dir/sci-results`

/afs/in2p3.fr/home/j/jmassot/public/compareSrc/job.py ${runs[$SGE_TASK_ID]}
