# -*- coding: utf-8 -*-

import sys
from parser import Drain

input_dir  = '../logs/web01/'
output_dir = '../data/'  # The output directory of parsing results
log_file   = 'error_web01.log'
#log_file   = 'error_all.log'
#log_format = '<Date> <Time> \[<Level>\] <Pid>\#[0-9]: \*<Seq> <Content>' 
log_format = '<Date> <Time> \[<Level>\] <Pid>\#[0-9]: <Content>' 

# Regular expression list for optional preprocessing (default: [])
regex      = [
    #r'blk_(|-)[0-9]+' , # block id
    r'((?<=[^A-Za-z0-9])|^)((\/[A-Za-z0-9\-\_\.]+)+\/[A-Za-z0-9\-\_.&=?%/]+)((?=[^A-Za-z0-9])|$)', # uri
    r'((?<=[^A-Za-z0-9])|^)([A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)+)((?=[^A-Za-z0-9])|$)', # domain name
    r'((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)', # IP
    r'((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)', # Numbers
    r'((?<=[^A-Za-z0-9])|^)(0x[a-f0-9A-F]+)((?=[^A-Za-z0-9])|$)', # HEX
    r'((?<=[^A-Za-z0-9])|^)([GET|POST|PATCH|PUT|DELETE]+)((?=[^A-Za-z0-9])|$)', # method
    #r'((?<=[^A-Za-z0-9])|^)(([0-9a-f]{2,}:){3,}([0-9a-f]{2,}))((?=[^A-Za-z0-9])|$)', # ID
    #r'((?<=[^A-Za-z0-9])|^)([0-9a-f]{6,} ?){3,}((?=[^A-Za-z0-9])|$)', # SEQ
    #r'((?<=[^A-Za-z0-9])|^)([0-9A-F]{4} ?){4,}((?=[^A-Za-z0-9])|$)', # SEQ
]
st         = 0.5  # Similarity threshold
depth      = 4  # Depth of all leaf nodes

parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
parser.parse(log_file)

