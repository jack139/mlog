# -*- coding: utf-8 -*-
''' This is a demo file for the Invariants Mining model.
    API usage:
        dataloader.load_HDFS(): load HDFS dataset
        feature_extractor.fit_transform(): fit and transform features
        feature_extractor.transform(): feature transform after fitting
        model.fit(): fit the model
        model.predict(): predict anomalies on given data
        model.evaluate(): evaluate model accuracy with labeled data
'''

import sys
from loglizer.models import InvariantsMiner
from loglizer import dataloader, preprocessing

struct_log = '../data/mongodb.log.1_structured.csv' # The structured log file
#label_file = '../data/anomaly_label_error_all.log.csv' # The anomaly label file
epsilon = 0.5 # threshold for estimating invariant space

if __name__ == '__main__':
    # Load structured log without label info
    (x_train, _), (x_test, _), _ = dataloader.load_HDFS(struct_log,
                                                     window='session', 
                                                     train_ratio=0.8,
                                                     split_type='uniform')
                                                     #split_type='sequential')
    # Feature extraction
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train)

    # Model initialization and training
    model = InvariantsMiner(epsilon=epsilon)
    model.fit(x_train)

    # Predict anomalies on the training set offline, and manually check for correctness
    y_train = model.predict(x_train)

    # Predict anomalies on the test set to simulate the online mode
    # x_test may be loaded from another log file
    x_test = feature_extractor.transform(x_test)
    y_test = model.predict(x_test)

    print(y_test)

    # If you have labeled data, you can evaluate the accuracy of the model as well.
    # Load structured log with label info
    #(x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(struct_log,
    #                                                           label_file=label_file,
    #                                                           window='session', 
    #                                                           train_ratio=0,
    #                                                           split_type='uniform')   
    #x_test = feature_extractor.transform(x_test)
    #precision, recall, f1 = model.evaluate(x_test, y_test)


