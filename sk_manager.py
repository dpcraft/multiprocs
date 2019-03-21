#!/Users/dpcraft/code/PythonWorkplace/tensorflow/bin/python3.6
# encoding:utf8
import queue
from multiprocessing.managers import BaseManager
from sklearn import datasets
from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from trans import Trans
import pandas as pd
import time
# from config import worker_num
# from config import contaminated_node_index
worker_num = 20
contaminated_node_index = []


# 返回污染数据集编号：
def check(a):
    s = set()
    for i in a:
        if ((i % worker_num) + 1) not in a:
            s.add((i % worker_num) + 1)
        if ((i - 2 + worker_num) % worker_num + 1) not in a:
            # print(i)
            s.add(i)
    print('污染数据集编号： ', s)
    return s


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


def get_mean(ar):
    aar = np.squeeze(np.array(ar))
    m_ = np.mean(aar, axis=0)
    return m_


def test():
    print(worker_num, contaminated_node_index)

# w_n:工作节点数
# c_n_i 污染节点下标
# xx 返回结果的索引，用来标记一组结果，最后用来平均
def manager_start(w_n, c_n_i, xx, return_dict_1, return_dict_2, return_dict_3):
    global worker_num, contaminated_node_index
    worker_num = w_n
    contaminated_node_index = c_n_i
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
    manager = QueueManager(address=('', 5000), authkey=b'abc', )
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    index = manager.get_index_queue()
    result = manager.get_result_queue()

    # worker的数目:
    # worker_num = 50
    for i in range(worker_num):
        index.put(2 * i + 1)
    print("开始读取数据")
    time_1 = time.time()
    # MINST数据集
    raw_data = pd.read_csv('./data/train_binary.csv', header=0)  # 读取csv数据，并将第一行视为表头，返回DataFrame类型
    data = raw_data.values
    X = data[::, 1::]
    y = data[::, 0]
    time_2 = time.time()
    print("读取数据完成")
    print("读取数据耗时%f 秒" % (time_2 - time_1))
    print(X.shape)
    print(y.shape)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    tmp = generate_queue(X_train, y_train, worker_num)
    while not tmp.empty():
        task.put(tmp.get())
    # 从result队列读取结果:
    # print('Try get results...')
    result_W1 = []
    result_W2 = []
    contaminated_result_W1 = []
    contaminated_result_W2 = []
    result_b1 = []
    result_b2 = []
    contaminated_result_b1 = []
    contaminated_result_b2 = []
    result_dict = {}
    for i in range(worker_num):
        r = result.get(timeout=300)
        result_dict[int(r.id)] = r
        # print('Result: %s' % i)
        # print(r.Wb1.W)

    # 不一致数据集编号
    s = check(contaminated_node_index)
    # for k, v in result_dict.items():
    for i in range(worker_num):
        v = result_dict[i + 1]
        # print(v.Wb1.b)
        result_W1.append(v.Wb1.W)
        result_b1.append(v.Wb1.b)
        result_W2.append(v.Wb2.W)
        result_b2.append(v.Wb2.b)
        # 备份污染后的结果
        if (i + 1) not in s:
            contaminated_result_W1.append(v.Wb1_contaminated.W)
            contaminated_result_b1.append(v.Wb1_contaminated.b)
        else:
            contaminated_result_W1.append(v.Wb1.W)
            contaminated_result_b1.append(v.Wb1.b)
        # 单节点污染后的结果
        contaminated_result_W2.append(v.Wb1_contaminated.W)
        contaminated_result_b2.append(v.Wb1_contaminated.b)


    manager.shutdown()
    # print('#' * 50)

    W_ = get_mean(result_W1)
    b_ = get_mean(result_b1)
    # print('*' * 20)
    # print('W_')
    # print(W_)
    # print('*' * 20)
    # print('b_')
    # print(b_)
    # print('*' * 20)
    l = []
    l.append(b_)
    clf = svm.LinearSVC()
    clf.coef_ = W_[np.newaxis, :]
    clf.intercept_ = np.array(l)
    print('参数W')
    print(clf.coef_)
    print('参数b')
    print(clf.intercept_)

    clf.classes_ = np.array([0, 1])
    score1 = clf.score(X_test, y_test)
    print("分布式训练正确率：")
    print(score1)


    # contaminated_W_2 = get_mean(contaminated_result_W2)
    # contaminated_b_2 = get_mean(contaminated_result_b2)
    # contaminated_l2 = []
    # contaminated_l2.append(contaminated_b_2)
    # clf4 = svm.LinearSVC()
    # clf4.coef_ = contaminated_W_2[np.newaxis, :]
    # clf4.intercept_ = np.array(contaminated_l2)
    # clf4.classes_ = np.array([0, 1])
    # score2 = clf4.score(X_test, y_test)
    # print("单节点节点污染后分布式训练正确率：")
    # print(score2)
    #
    # clf2 = svm.LinearSVC()
    # clf2.fit(X_train, y_train)
    # print("单机训练正确率：")
    # print(clf2.score(X_test, y_test))
    # print('W:', clf2.coef_, 'b: ', clf2.intercept_)


    return_dict_1[xx] = score1
    # return_dict_2[xx] = score2
    exit(0)


if __name__ == '__main__':
    manager_start()




