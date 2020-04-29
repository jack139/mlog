### MLog (Machine learning Log analysis)

生成日志模板
`python3 paring_log`

IM测试
`python3 InvariantsMiner_without_labels.py`

PCA测试
`python3 PCA_without_labels.py`



单机版：

实时日志 --> 日志抓取脚本 --> MLog



多机版：

实时日志 --> flume --> Kafka --> MLog