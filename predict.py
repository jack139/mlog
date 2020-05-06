#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from parser import Drain

#input_dir  = 'logs/web01/'
output_dir = 'data/rt'  # The output directory of parsing results
#log_file   = 'error_web01.log'
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


#sys.path.append('../')
from loglizer.models import InvariantsMiner
from loglizer import dataloader, preprocessing

#test_struct_log = 'data/error_web01.log_structured.csv' # The structured log file
#test_label_file = 'data/anomaly_label_error_web01.log.csv' # The anomaly label file

epsilon = 0.5 # threshold for estimating invariant space



if __name__ == '__main__':
    if len(sys.argv)<2:
        print("usage: python %s <log_file>" % sys.argv[0])
        sys.exit(2)

    log_file = sys.argv[1]

    # 分析日志
    input_dir, log_filename = os.path.split(log_file)
    parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)    
    parser.parse(log_filename)

    struct_log = os.path.join(output_dir, log_filename + '_structured.csv')

    # 预测计算
    # load model and feature object from file
    model = dataloader.load_object('train/IM.model')
    feature_extractor = dataloader.load_object('train/IM.feature')

    (x_train, _), (x_test, _), _ = dataloader.load_HDFS(struct_log,
                                                     window='session', 
                                                     train_ratio=0,
                                                     split_type='uniform')
                                                     #split_type='sequential')

    x_test = feature_extractor.transform(x_test)

    y_test = model.predict(x_test)
    print(y_test)
