#!/bin/sh

MLOG_DIR="."
LOG_PATH="logs/wechat_test"
STARTER="yktWechat_error"


start_back() {
	nohup python3 $MLOG_DIR"/backrun.pyc" $MLOG_DIR $LOG_PATH $STARTER >> "/tmp/backrun.log" &
	return 0 
}

stop_back() {
	kill `pgrep -f "backrun.py"`
	return 0
}

status() {
	ps -f -C python3 -C tail
	return 0
}

restart() {
	stop_back
	sleep 1
	start_back
}


case "$1" in
	start)
		start_back
		RETVAL=$?
	;;
	stop)
		stop_back
		RETVAL=$?
	;;
	restart)
		restart
		RETVAL=$?
	;;
	status)
		status
		RETVAL=$?
	;;
	*)
	echo $"Usage: run.sh start|stop|restart|status"
	RETVAL=2
	;;
esac

exit $RETVAL
