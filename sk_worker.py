#!/Users/dpcraft/code/PythonWorkplace/tensorflow/bin/python3.6
# encoding:utf8

import time
import sys
import queue
from multiprocessing.managers import BaseManager
from sklearn import svm
from params import Params
from params import Wb
from config import contaminated_node_index
import numpy as np
from config import worker_num
import copy


# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass


# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
QueueManager.register('get_index_queue')

# 连接到服务器，也就是运行taskmanager.py的机器:
server_addr = '127.0.0.1'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
# 从网络连接:
m.connect()
# 获取Queue的对象:
index = m.get_index_queue()
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:
# for i in range(10):
# while not task.empty():
#     X = task.get(timeout=10)
#     print(X.data)
#     print(X.target)
    # try:
    #     n = task.get(timeout=1)
    #     print('run task %d * %d...' % (n, n))
    #     r = '%d * %d = %d' % (n, n, n*n)
    #     time.sleep(1)
    #     result.put(r)
    # except queue.Empty:
    #     print('task queue is empty.')
if not index.empty():
    task_index = index.get(timeout=1)
else:
    print("no task")
    exit(0)
node_num = (worker_num - (task_index - 1)/2)
print('节点编号：%d' % node_num)
# print('任务编号：%d ' % task_index)
# 客户端存储队列
client_queue = queue.Queue()
client_d = []
while not task.empty():
    # print(task.qsize == task_index)
    if task.qsize() == task_index or task.qsize() == task_index + 1:
        X = task.get(timeout=1)
        # client_queue.put(X)
        client_d.append(X)
        # print(X.target)

# 创建一个数据副本用来污染
client_d_contaminated = copy.deepcopy((client_d))


def contaminate_data(d):
    print(d.target.shape)
    # d.target = np.ones(shape=d.target.shape) - d.target
    d.target = 1 - d.target
    return d


Wb1 = Wb([[]], [])
Wb2 = Wb([[]], [])
Wb1_contaminated = Wb([[]], [])
Wb2_contaminated = Wb([[]], [])


def train(data_collection):
    # 数据集编号
    data_no = 0
    # 计数变量
    no = 1
    for i in data_collection:
        clf = svm.LinearSVC()
        clf.fit(i.data, i.target)
        # print(clf.get_params())
        if no == 1:
            Wb_tmp_1 = Wb(W=clf.coef_, b=clf.intercept_)
            data_no = node_num
        else:
            Wb_tmp_2 = Wb(W=clf.coef_, b=clf.intercept_)
            data_no = (node_num + 1) % worker_num
        print('数据D_%d ' % data_no)
        # print('y_: ')
        # print(i.target)
        print('w: ')
        print(clf.coef_)
        print('b: ')
        print(clf.intercept_)
        no = no + 1
    return Wb_tmp_1, Wb_tmp_2


print('未污染的数据训练结果：')
Wb1, Wb2 = train(client_d)
print('*' * 50)


if node_num in contaminated_node_index:
    print('污染数据')
    for i in client_d_contaminated:
        # print('污染前：')
        # print(i.target)
        i = contaminate_data(i)
        # print('污染后：')
        # print(i.target)

print('污染后的数据训练结果：')
Wb1_contaminated, Wb2_contaminated = train(client_d_contaminated)


result.put(Params(id=node_num, Wb1=Wb1, Wb2=Wb2, Wb1_contaminated=Wb1_contaminated, Wb2_contaminated= Wb2_contaminated))
# result.put(task_index + 1)

# 处理结束:
print('worker exit.')
