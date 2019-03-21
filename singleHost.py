from sklearn import svm
import numpy as np
import time
from sklearn.model_selection import train_test_split
import pandas as pd


print("开始读取数据")
time_1 = time.time()
# MINST数据集
raw_data = pd.read_csv('./data/train.csv', header=0)  # 读取csv数据，并将第一行视为表头，返回DataFrame类型
data = raw_data.values
X = data[::, 1::]
y = data[::, 0]
raw_data2 = pd.read_csv('./data/train_2.csv', header=0)  # 读取csv数据，并将第一行视为表头，返回DataFrame类型
data2 = raw_data.values
X2 = data2[::, 1::]
y2 = data2[::, 0]
time_2 = time.time()
print("读取数据完成")
print("读取数据耗时%f 秒" % (time_2 - time_1))
print(X.shape)
print(y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9998)
clf2 = svm.LinearSVC()
# clf2.fit(X_train, y_train)
clf2.fit(X2, y2)
print('W:', clf2.coef_, 'b: ', clf2.intercept_)
print("单机训练正确率：")
print(clf2.score(X_test, y_test))
