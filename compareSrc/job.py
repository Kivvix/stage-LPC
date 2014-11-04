#!/usr/bin/env python
# -*- coding: utf-8 -*-

## @package compareSrc
#  @author J. Massot
#  @date 2014-06-20

from config import *
import os, sys
import compareSrc

runNum = sys.argv[1]


compareSrc.d( runNum )

compareSrc.c(  runNum )

compareSrc.s( runNum )
