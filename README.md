## MLog (Machine learning Log analysis)

生成日志模板
`train/python3 paring_log`

IM测试
`train/python3 InvariantsMiner_without_labels.py`

PCA测试
`train/python3 PCA_without_labels.py`



### 单机版：

实时日志 --> 日志抓取脚本 --> MLog

##### 训练过程：

日志文件 --> 日志模板 --> 根据窗口设置生成日志数据 --> 训练模型

`python3 train_IM.py`

##### 预测过程：

日志文件 --> bash脚本 --> stdin
log --> 生成模板 --> 比对是否有新模板
根据窗口设置生成日志数据 --> 使用模型预测

`cat logs/nginx/error.log | python3 mlog.py`

`python3 predict.py logs/rt/20200417_07.log`

### 多机版：

实时日志 --> flume --> Kafka --> MLog
