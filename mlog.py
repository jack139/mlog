#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 从stdin读入数据, 例如使用管道：
# tail -f nginx/logs/uwsgi_wx.log | python echo_test.py
#

import sys, os
import subprocess

out_dir = './logs/rt'

# 根据时间日期获取 label
# 参考格式： 2020/04/17 07:09:27 [error] 26119#0: ...
def get_nginx_error_label(log):
    log_split = log.split()
    date = log_split[0].replace('/','')
    time = log_split[1].split(':')
    #return '%s_%s_%s'%(date, time[0], time[1])  # 20200417_07_09 按 分钟
    return '%s_%s'%(date, time[0])  # 20200417_07 按 小时


if __name__ == '__main__':
    current_label = file = process = None

    for line in sys.stdin:
        if (len(line.split('\n\r'))>1): # 检查是否存在一次多行，按说不应该
            print('WARNING: more than one line!')
            print(line.split('\n\r'))

        label = get_nginx_error_label(line)
        if label != current_label:
            if file: # 第一次时不需要close 
                file.close()
                # 生成一个日志集合，开始预测计算
                print(filepath)
                process = subprocess.Popen('python3 predict.py '+filepath, shell=True)
                    #stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            current_label = label
            filepath = os.path.join(out_dir, current_label + '.log')
            file = open(filepath, 'w')
        
        file.write(line)
        file.flush()

    # 结束
    if file:
        file.close()
        process = subprocess.Popen('python3 predict.py '+filepath, shell=True)
            #stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print('wait process end ...')
        retcode = process.wait()
        print(retcode)

