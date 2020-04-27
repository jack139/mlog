#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from parser import Drain

input_dir  = 'logs/nginx/'
output_dir = 'result/'  # The output directory of parsing results
log_file   = 'uwsgi_wx.log'
log_format = '\[pid: <Pid>\|app: <App>\|req: <Req>\] <IP> \(\) \{<vars> vars in <Bytes> bytes\} \[<Day> <Mon> <Date> <Time> <Year>\] <Content>' 

# Regular expression list for optional preprocessing (default: [])
regex      = [
    #r'blk_(|-)[0-9]+' , # block id
    #r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
    r'((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)', # IP
    #r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
    r'((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)', # Numbers
    r'((?<=[^A-Za-z0-9])|^)(0x[a-f0-9A-F]+)((?=[^A-Za-z0-9])|$)', # HEX
    r'((?<=[^A-Za-z0-9])|^)(([0-9a-f]{2,}:){3,}([0-9a-f]{2,}))((?=[^A-Za-z0-9])|$)', # ID
    r'((?<=[^A-Za-z0-9])|^)([0-9a-f]{6,} ?){3,}((?=[^A-Za-z0-9])|$)', # SEQ
    r'((?<=[^A-Za-z0-9])|^)([0-9A-F]{4} ?){4,}((?=[^A-Za-z0-9])|$)', # SEQ
]
st         = 0.5  # Similarity threshold
depth      = 4  # Depth of all leaf nodes

parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser.parse(log_file)

