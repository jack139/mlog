# -*- coding: utf-8 -*-

# 从stdin读入数据, 例如使用管道：
# tail -f nginx/logs/uwsgi_wx.log | python echo_test.py
#

import sys, os
import predict

out_dir = './logs/rt'

# 根据时间日期获取 label
# 参考格式： 2020/04/17 07:09:27 [error] 26119#0: ...
def get_nginx_error_label(log, minute=60): # 按min分钟为间隔，默认是60分钟 
    log_split = log.split()
    if len(log_split)<2: # 可能是空行
        return None
    date = log_split[0].replace('/','')
    time = log_split[1].split(':')
    q = int(time[1])//minute
    return '%s_%s_%d'%(date, time[0], q)  # 20200417_07_1 按间隔返回


# 使用log进行预测
def predict_it(log_lines, label):
    struct_log = predict.parse_log(log_lines)
    y_test = predict.predict_IM(struct_log)
    print(y_test)
    if y_test[0]==1: # 出现异常，保存日志
        filepath = os.path.join(out_dir, 'anomaly_'+label+'.log') 
        with open(filepath, 'w') as f:
            f.write(''.join(log_lines))
        print('-------------------->>>> ANOMALY detected:', filepath)


if __name__ == '__main__':
    current_label = None
    log_lines = []

    for line in sys.stdin:
        if (len(line.split('\n\r'))>1): # 检查是否存在一次多行，按说不应该
            print('WARNING: more than one line!')
            print(line.split('\n\r'))

        label = get_nginx_error_label(line, 15)
        if label is None:
            continue
        if label != current_label:
            # 生成一个日志集合，开始预测计算
            if len(log_lines)>0:
                predict_it(log_lines, current_label)
            current_label = label
            log_lines = []
            print(current_label)

        log_lines.append(line)

    # 结束
    if len(log_lines)>0:
        predict_it(log_lines, current_label)



