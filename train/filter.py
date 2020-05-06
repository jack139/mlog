# -*- coding: utf-8 -*-

import sys, os

#input_dir  = 'logs/nginx/'
#log_file   = 'uwsgi_wx.log.20200418'
#output_dir = 'logs/nginx/'  
#output_file = 'uwsgi_wx2.log'

#with open(os.path.join(input_dir, log_file), 'r') as f1, \
#        open(os.path.join(output_dir, output_file), 'w') as f2:
#    line = f1.readline()
#    c=1
#    while line:
#        if line[:5] == '[pid:':
#            f2.write(line)
#            c += 1
#        line = f1.readline()
#
#print('saved lines: ', c)


log_dir = 'logs/web01'
output_file = 'error_web01.log'

file_list = os.listdir(log_dir)
with open(os.path.join(log_dir, output_file), 'w') as f1:
    for f in file_list:
        with open(os.path.join(log_dir, f), 'r') as f2:
            f1.write(f2.read())
