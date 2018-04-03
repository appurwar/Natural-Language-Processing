#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 16:04:33 2018

@author: apoorv
"""

import sys
import os

if sys.argv[1] == 'q4':
    os.system('python count_cfg_freq.py ' + sys.argv[2] + ' > cfg.counts')
    os.system('./q4.py ' + sys.argv[2] + ' ' + sys.argv[3])
elif(sys.argv[1] == 'q5'):
    os.system('python count_cfg_freq.py ' + sys.argv[2] + ' > cfg_rare_q5.counts')
    os.system('./q5.py ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4])
    os.system('python eval_parser.py parse_dev.key ' + sys.argv[4] + ' > q5_eval.txt')    
elif(sys.argv[1] == 'q6'):
    os.system('python count_cfg_freq.py ' + sys.argv[2] + ' > cfg_rare_q6.counts')
    os.system('./q6.py ' + sys.argv[2] + ' ' + sys.argv[3] + ' ' + sys.argv[4])
    os.system('python eval_parser.py parse_dev.key ' + sys.argv[4] + ' > q6_eval.txt')    