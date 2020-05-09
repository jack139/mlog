# -*- coding: utf-8 -*-
#
# 后台daemon进程，启动后台处理进程，并检查进程监控状态
#

import sys
import time, os
import signal

MLOG_DIR=''
LOG_DIR=''
STARTER=None

def start_processor(pname, log_file):
    cmd0="nohup tail -f %s/%s | python3 %s/mlog.pyc /tmp/anomaly_log > /tmp/mlog.log 2>&1 &" % \
        (LOG_DIR, log_file, MLOG_DIR)
    print(cmd0)
    os.system(cmd0)

def get_processor_pid(pname):
    cmd0='pgrep -f "%s"' % pname
    #print cmd0
    pid=os.popen(cmd0).readlines()
    if len(pid)>0:
        return pid[0].strip()
    else:
        return None

def kill_processor(pname):
    cmd0='kill -9 `pgrep -f "%s"`' % pname
    #print cmd0
    os.system(cmd0)
    time.sleep(1)


# 按修改时间顺序返回文件列表
def get_file_list(file_path, starter=None):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        # print(dir_list)
        if starter is not None:
            dir_list = [i for i in dir_list if i.startswith(starter)]
        return dir_list

# 捕捉停止信号，对 kill -9 无效
def handler(signum, frame):
    kill_processor('%s/mlog.pyc' % MLOG_DIR)
    kill_processor('tail -f')
    print('Signal recieved:', signum)
    print("DAEMON: %s exited" % time.ctime())
    sys.exit(2)

signal.signal(signal.SIGTERM, handler) # kill
signal.signal(signal.SIGINT, handler)  # Ctrl-C


if __name__=='__main__':
    if len(sys.argv)<4:
        print("usage: daemon.py <MLOG_DIR> <LOG_DIR> <STARTER>")
        sys.exit(2)

    MLOG_DIR=sys.argv[1]
    LOG_DIR=sys.argv[2]
    STARTER=sys.argv[3]

    print("DAEMON: %s started" % time.ctime())
    print("MLOG_DIR=%s\nLOG_DIR=%s\nSTRATER=%s" % (MLOG_DIR, LOG_DIR, STARTER))

    #
    #启动后台进程
    #
    kill_processor('%s/mlog.pyc' % MLOG_DIR)
    kill_processor('tail -f')
    current_log = get_file_list(LOG_DIR, STARTER)[-1]
    start_processor('mlog', current_log)

    _count=_ins=0
    while 1:                        
        # 检查processor进程 backrun
        pid=get_processor_pid('%s/mlog.pyc' % MLOG_DIR)
        if current_log!=get_file_list(LOG_DIR, STARTER)[-1]: # 最新日志文件有变化
            pid=None
        if pid==None:
            # 进程已死, 重启进程
            kill_processor('%s/mlog.pyc' % MLOG_DIR)
            kill_processor('tail -f')
            current_log = get_file_list(LOG_DIR, STARTER)[-1]
            start_processor('mlog', current_log)
            _ins+=1
            print("%s\tbackrun restart" % time.ctime())
     
        time.sleep(5)
        if _count>1000:
            if _ins>0:
                print("%s  HEARTBEAT: error %d" % (time.ctime(), _ins))
            else:
                print("%s  HEARTBEAT: fine." % (time.ctime()))
            _count=_ins=0
        sys.stdout.flush()

