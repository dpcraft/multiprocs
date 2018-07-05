#!/Users/dpcraft/code/PythonWorkplace/tensorflow/bin/python3.6
# encoding:utf8
import random
import queue
from multiprocessing.managers import BaseManager
from sklearn import datasets
from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from trans import Trans
# 发送任务的队列:
task_queue = queue.Queue()
index_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_index_queue', callable=lambda: index_queue)
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('', 5000), authkey=b'abc',)
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
index = manager.get_index_queue()
result = manager.get_result_queue()

# worker的数目:
worker_num = 3
for i in range(worker_num):
    index.put(2 * i + 1)

# 任务分配函数
# |D1|D2|D2|D3|D3|D4|D4|...|Dn|Dn|D1|


def generate_queue(data, target, parts):
    q = queue.Queue()
    size = 1 / parts
    X_1, X_2, y_1, y_2 = train_test_split(data, target, test_size=size)
    d1 = Trans(data=X_2, target=y_2)
    q.put(d1)
    if parts == 2:
        q.put(Trans(data=X_1, target=y_1))
        q.put(Trans(data=X_1, target=y_1))
    data = X_1
    target = y_1
    parts = parts - 1
    while parts >= 2:
        size = 1 / parts
        X_1, X_2, y_1, y_2 = train_test_split(data, target, test_size=size)
        q.put(Trans(data=X_2, target=y_2))
        q.put(Trans(data=X_2, target=y_2))
        if parts == 2:
            q.put(Trans(data=X_1, target=y_1))
            q.put(Trans(data=X_1, target=y_1))
        data = X_1
        target = y_1
        parts = parts - 1
    q.put(d1)
    return q


# iris = datasets.load_iris()
# # print(iris)
# X = iris.data
# y = iris.target
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5)
# X_1_1, X_1_2, y_1_1, y_1_2 = train_test_split(X_1, y_1, test_size=.5)
# print('X_1_1:\n')
# print(X_1_1)
# print('y_1_1:\n')
# print(y_1_1)
# task.put(Trans(data=X_1_1, target=y_1_1))
# task.put(Trans(data=X_1_2, target=y_1_2))
r = np.load('./data/test_2_class.npz')
X = r['data']
y = r['target']
print(X.shape)
print(y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
tmp = generate_queue(X_train, y_train, worker_num)
while not tmp.empty():
    task.put(tmp.get())
print(task.qsize())
# while not task.empty():
#     print(task.get().target)

# for i in range(10):
#     n = random.randint(0, 10000)
#     print('Put task %d...' % n)
#     task.put(n)
# 从result队列读取结果:
print('Try get results...')
result_W = []
result_b = []
for i in range(worker_num):
    r = result.get(timeout=30)
    print('Result: %s' % r.id)
    result_W.append(r.Wb1.W)
    result_b.append(r.Wb1.b)
    # print(r.id)
    # print(type(r.Wb1.W))
    # print(type(r.Wb1.b))
    # print('r.Wb1.W')
    print(r.Wb1.W)
    # print('r.Wb1.b')
    # print(r.Wb1.b)
# 关闭:
manager.shutdown()
print('#' * 50)


def get_mean(ar):
    # print(ar)
    aar = np.squeeze(np.array(ar))
    print(aar.shape)
    print(aar)
    # m_ = np.zeros(np.squeeze(np.array(ar)).shape)
    # print(m_)
    # for i in ar:
    #     # print(i)
    #     m_ = m_ + i
    # print('m_')
    # print(m_)
    m_ = np.mean(aar, axis=0)
    return m_


# print('result_W')
# print(result_W)
# print(result_b)
# print('result_b')
W_ = get_mean(result_W)
b_ = get_mean(result_b)
print('*' * 20)
print('W_')
print(W_)
print('*' * 20)
print('b_')
print(b_)

print(W_[np.newaxis, :])
l =[]
l.append(b_)
print(np.array(l))
print(np.array(b_))
clf = svm.LinearSVC()
clf.coef_ = W_[np.newaxis, :]
clf.intercept_ = np.array(l)
clf.classes_ = np.array([0, 1])
print("分布式训练正确率：")
print(clf.score(X_test, y_test))

clf2 = svm.LinearSVC()
clf2.fit(X_train, y_train)
print("传统训练正确率：")
print(clf2.score(X_test, y_test))

