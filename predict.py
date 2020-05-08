# -*- coding: utf-8 -*-

import sys, os
from libs import Drain

output_dir = 'data/rt'  # The output directory of parsing results
#log_format = '<Date> <Time> \[<Level>\] <Pid>\#[0-9]: <Content>'  # nginx
log_format = '<Date> <Time>\,<mm> \[<Thread>\] <Level> <Content>'  # wechat manager

# Regular expression list for optional preprocessing (default: [])
regex      = [
    r'((?<=[^A-Za-z0-9])|^)((\/[A-Za-z0-9\-\_\.]+)+\/[A-Za-z0-9\-\_.&=?%/]+)((?=[^A-Za-z0-9])|$)', # uri
    r'((?<=[^A-Za-z0-9])|^)([A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)+)((?=[^A-Za-z0-9])|$)', # domain name
    r'((?<=[^A-Za-z0-9])|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})((?=[^A-Za-z0-9])|$)', # IP
    r'((?<=[^A-Za-z0-9])|^)([\-\+]?\d+)((?=[^A-Za-z0-9])|$)', # Numbers
    r'((?<=[^A-Za-z0-9])|^)(0x[a-f0-9A-F]+)((?=[^A-Za-z0-9])|$)', # HEX
    r'((?<=[^A-Za-z0-9])|^)([GETPOSTPATCHPUTDELETE]{1,6})((?=[^A-Za-z0-9])|$)', # method
    r'((?<=[^A-Za-z0-9])|^)(([0-9a-f]{2,}:){3,}([0-9a-f]{2,}))((?=[^A-Za-z0-9])|$)', # ID
    r'((?<=[^A-Za-z0-9])|^)([0-9a-f]{6,} ?){3,}((?=[^A-Za-z0-9])|$)', # SEQ
    r'((?<=[^A-Za-z0-9])|^)([0-9A-F]{4} ?){4,}((?=[^A-Za-z0-9])|$)', # SEQ
    r'((?<=[^A-Za-z0-9])|^)([wxgh\_]{1,3}[a-f0-9A-F]+)((?=[^A-Za-z0-9])|$)', # 微信ID
]
st         = 0.5  # Similarity threshold
depth      = 4  # Depth of all leaf nodes


#from libs.models import InvariantsMiner
from libs import dataloader #, preprocessing

epsilon = 0.5 # threshold for estimating invariant space

period = 15 # 数据划分时间间隔

# 已训练的模型
trained_model = dataloader.load_object('IM.model')
trained_feature = dataloader.load_object('IM.feature')
trained_templates = dataloader.load_object('IM.templates')


# 使用参数方式传递

# 分析日志
def parse_log(log_lines):
    parser = Drain.LogParser(log_format, outdir=output_dir, depth=depth, st=st, rex=regex, save_csv=False)
    struct_log, templates = parser.parse(logLines=log_lines)
    unknown_templates = []
    for i in templates:
        if i[0] not in trained_templates:
            unknown_templates.append('%s %s\n'%(i[0],i[1]))
            print('>>>>>>>>>>>>>>>>>>>>>>>>> UNKNOWN templates:', i[0], i[1])
    return struct_log, unknown_templates

def parse_log_file(log_file):
    input_dir, log_filename = os.path.split(log_file)
    parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)    
    _, templates_id = parser.parse(log_filename)
    struct_log = os.path.join(output_dir, log_filename + '_structured.csv')
    return struct_log, templates_id

# 预测计算
def predict_IM(struct_log):
    # 预测计算
    # load model and feature object from file
    model = trained_model
    feature_extractor = trained_feature

    (x_train, _), (x_test, _), _ = dataloader.load_HDFS(df_log=struct_log,
                                                    window='session', 
                                                    train_ratio=0,
                                                    period=period,
                                                    split_type='uniform')
                                                    #split_type='sequential')
    x_test = feature_extractor.transform(x_test)

    y_test = model.predict(x_test)
    return y_test


# 使用文件方式传递参数，进行计算
if __name__ == '__main__': 
    if len(sys.argv)<2:
        print("usage: python %s <log_file>" % sys.argv[0])
        sys.exit(2)

    log_file = sys.argv[1]

    # 分析日志
    struct_log = parse_log_file(log_file)

    # 预测计算
    # load model and feature object from file
    model = dataloader.load_object('IM.model')
    feature_extractor = dataloader.load_object('IM.feature')

    (x_train, _), (x_test, _), _ = dataloader.load_HDFS(struct_log,
                                                    window='session', 
                                                    train_ratio=0,
                                                    period=period,
                                                    split_type='uniform')
                                                    #split_type='sequential')
    x_test = feature_extractor.transform(x_test)

    y_test = model.predict(x_test)
    print(y_test)
