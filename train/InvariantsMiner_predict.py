# -*- coding: utf-8 -*-

import sys
#sys.path.append('../')
from loglizer.models import InvariantsMiner
from loglizer import dataloader, preprocessing

test_struct_log = '../data/wechat2.log_structured.csv' # The structured log file
#test_label_file = '../data/anomaly_label_error_web01.log.csv' # The anomaly label file

epsilon = 0.5 # threshold for estimating invariant space

if __name__ == '__main__':

    # load model and feature object from file
    model = dataloader.load_object('IM.model')
    feature_extractor = dataloader.load_object('IM.feature')

    #(x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(test_struct_log,
    #                                                           label_file=test_label_file,
    #                                                           window='session', 
    #                                                           train_ratio=0,
    #                                                           split_type='uniform')   
    (x_train, _), (x_test, _), _ = dataloader.load_HDFS(test_struct_log,
                                                     window='session', 
                                                     train_ratio=0.0,
                                                     save_csv=True,
                                                     split_type='uniform')
                                                     #split_type='sequential')

    x_test = feature_extractor.transform(x_test)
    #precision, recall, f1 = model.evaluate(x_test, y_test)

    y_test = model.predict(x_test)
    print(y_test)
