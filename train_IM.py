# -*- coding: utf-8 -*-

import sys
from libs.models import InvariantsMiner
from libs import dataloader, preprocessing

struct_log = 'data/error_all.log_structured.csv' # The structured log file
label_file = 'data/anomaly_label_error_all.log.csv' # The anomaly label file
epsilon = 0.5 # threshold for estimating invariant space

if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(struct_log,
                                                                label_file=label_file,
                                                                window='session', 
                                                                train_ratio=1,
                                                                save_csv=True,
                                                                split_type='uniform')
                                                                #split_type='sequential')
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train)
    x_test = feature_extractor.transform(x_test)

    model = InvariantsMiner(epsilon=epsilon)
    model.fit(x_train)

    print('Train validation:')
    precision, recall, f1 = model.evaluate(x_train, y_train)
    
    #print('Test validation:')
    #precision, recall, f1 = model.evaluate(x_test, y_test)

    #y_test = model.predict(x_test)
    #print(y_test)

    # save model and feature object
    dataloader.save_object(model, 'IM.model')
    dataloader.save_object(feature_extractor, 'IM.feature')
