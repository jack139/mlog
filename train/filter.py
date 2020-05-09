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


# 合并
#log_dir = 'logs/webchat'
#output_file = 'error_web01.log'
#
#file_list = os.listdir(log_dir)
#with open(os.path.join(log_dir, output_file), 'w') as f1:
#    for f in file_list:
#        with open(os.path.join(log_dir, f), 'r') as f2:
#            f1.write(f2.read())

# java 日志去掉异常
log_dir = '../logs/wechat'
file_list = os.listdir(log_dir)
for f in file_list:
    if f.startswith('new_'):
        continue
    f2 = 'new_'+f
    with open(os.path.join(log_dir, f), 'r') as ff, \
            open(os.path.join(log_dir, f2), 'w') as ff2:
        line = ff.readline()
        c=1
        last_dt = ''
        while line:
            if line[0] != '\t': # 异常终端内容，忽略
                if line[0].isdigit(): # 正常格式日志
                    l2 = line.split()
                    last_dt = l2[0]+' '+l2[1]
                else: # java异常，首行
                    line = last_dt + ' [-] ERROR ' + line

                ff2.write(line)
                c += 1

            line = ff.readline()

    print('%s: %d'%(f, c))


# 合并
output_file = 'wechat.log'

file_list = os.listdir(log_dir)
file_list = sorted(file_list)
with open(os.path.join(log_dir, output_file), 'w') as f1:
    for f in file_list:
        if f.startswith('new_'):
            print(f)
            with open(os.path.join(log_dir, f), 'r') as f2:
                f1.write(f2.read())
