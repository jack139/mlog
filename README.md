# MLog (Machine learning Log analysis)

生成日志模板
`python3 paring_log`

IM测试
`python3 InvariantsMiner_without_labels.py`

PCA测试
`python3 PCA_without_labels.py`



##单机版：
实时日志 --> 日志抓取脚本 --> MLog

###训练过程：
日志文件 --> 日志模板 --> 根据窗口设置生成日志数据 --> 训练模型

###预测过程：
日志文件 --> bash脚本 --> stdin
log --> 生成模板 --> 比对是否有新模板
根据窗口设置生成日志数据 --> 使用模型预测


##多机版：

实时日志 --> flume --> Kafka --> MLog
