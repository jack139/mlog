#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os

input_dir  = 'logs/nginx/'
log_file   = 'uwsgi_wx.log.20200418'
output_dir = 'logs/nginx/'  
output_file = 'uwsgi_wx2.log'

with open(os.path.join(input_dir, log_file), 'r') as f1, \
        open(os.path.join(output_dir, output_file), 'w') as f2:
    line = f1.readline()
    c=1
    while line:
        if line[:5] == '[pid:':
            f2.write(line)
            c += 1
        line = f1.readline()

print('saved lines: ', c)
