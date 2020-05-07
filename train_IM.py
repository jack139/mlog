# -*- coding: utf-8 -*-

import sys
from libs.models import InvariantsMiner
from libs import dataloader, preprocessing
from predict import parse_log_file

#log_file = 'logs/web01/error_web01.log'
#label_file = 'data/anomaly_label_error_all.log.csv' # The anomaly label file  IM 训练实际不需要标签
epsilon = 0.5 # threshold for estimating invariant space

if __name__ == '__main__':
    if len(sys.argv)<2:
        print("usage: python %s <log_file>" % sys.argv[0])
        sys.exit(2)

    log_file = sys.argv[1]

    # 分析日志
    struct_log, templates = parse_log_file(log_file)

    # 装入训练数据
    #(x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(struct_log,
    #                                                            label_file=label_file,
    #                                                            window='session', 
    #                                                            train_ratio=1,
    #                                                            save_csv=True,
    #                                                            split_type='uniform')
    #                                                            #split_type='sequential')
    (x_train, _), (x_test, _), _ = dataloader.load_HDFS(struct_log,
                                                    window='session', 
                                                    train_ratio=1,
                                                    save_csv=True,
                                                    split_type='sequential')

    # 抽取特征
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train)
    x_test = feature_extractor.transform(x_test)

    # 训练模型
    model = InvariantsMiner(epsilon=epsilon)
    model.fit(x_train)

    # 训练数据评估
    #print('Train validation:')
    #precision, recall, f1 = model.evaluate(x_train, y_train)
    
    #print('Test validation:')
    #precision, recall, f1 = model.evaluate(x_test, y_test)

    #y_test = model.predict(x_test)
    #print(y_test)

    # 只保存模板id
    templates_id = []
    for i in templates:
        templates_id.append(i[0])

    # 保存模型和特征
    dataloader.save_object(model, 'IM.model')
    dataloader.save_object(feature_extractor, 'IM.feature')
    dataloader.save_object(templates_id, 'IM.templates')
