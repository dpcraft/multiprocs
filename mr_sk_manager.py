#!/Users/dpcraft/code/PythonWorkplace/tensorflow/bin/python3.6
# encoding:utf8
import queue
from multiprocessing.managers import BaseManager
from sklearn import datasets
from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from trans import Trans
import math
import random
# from config import worker_num
# from config import contaminated_node_index
worker_num = 20
circle_no = 10
contaminated_node_index = []


def real_check(result_dict):

    s = set()
    i = 0
    while i < (len(result_dict) - 1):
        # print(i, len(result_dict) - 1)
        res1 = result_dict[i + 1]
        res2 = result_dict[i + 2]
        # print('res1.Wb1.W - res2.Wb2.W')
        # print(res1.Wb1.W)
        # print(res2.Wb2.W)
        # print(res1.Wb1.W - res2.Wb2.W)
        # print('res1.Wb2.W - res2.Wb1.W')
        # print(res1.Wb2.W - res2.Wb1.W)
        if check_threshold(res1.Wb1_contaminated.W - res2.Wb2_contaminated.W, res1.Wb2_contaminated.W - res2.Wb1_contaminated.W):
            s.add(i + 1)
            s.add(i + 2)
            print(res1.Wb1.W)
            print(res1.Wb1_contaminated.W)
            # print('res1.Wb1.W - res2.Wb2.W')
            # print(res1.Wb1.W - res2.Wb2.W)
            # print('res1.Wb2.W - res2.Wb1.W')
            # print(res1.Wb2.W - res2.Wb1.W)
        i = i + 2
    return s


def check_threshold(a1, a2):
    threshold = 0.0001
    min1 = abs(np.min(a1))
    min2 = abs(np.min(a2))
    max1 = abs(np.max(a1))
    max2 = abs(np.max(a2))
    # print(min1, min2, max1, max2)
    # print(min1 > threshold)
    # print(min2 > threshold)
    # print(max1 > threshold)
    # print(max2 > threshold)
    # print((min1 > threshold) or (min2 > threshold) or (max1 > threshold) or (max2 > threshold))
    return (min1 > threshold) or (min2 > threshold) or (max1 > threshold) or (max2 > threshold)





# 返回污染数据集编号：
def check(a, worker_circle):
    s = set()
    for i in a:
        if ((i % worker_circle) + 1) not in a:
            s.add((i % worker_circle) + 1)
        if ((i - 2 + worker_circle) % worker_circle + 1) not in a:
            # print(i)
            s.add(i)
    # print('污染数据集编号： ', s)
    return s


def mr_check(a):
    mr_s = []
    workers_each_circle = splitInteger(worker_num, circle_no)
    offsets = []
    print('每个环的worker数目： ', workers_each_circle)
    # 偏移量->该环上的worker数目的dict
    offset_to_worker_num = {}
    offset = 0
    offsets.append(offset)
    for i in range(len(workers_each_circle)):
        offset_to_worker_num[offset] = workers_each_circle[i]
        offset += workers_each_circle[i]
        offsets.append(offset)
    # print(offset_to_worker_num)
    # print('offsets:', offsets)
    # a1是偏移量->数据编号的dict
    a1 = {}
    for ofs in offsets:
        a1[ofs] = []

    for aa in a:
        for i in range(1, len(offsets)):
            if aa <= offsets[i]:
                a1[offsets[i-1]].append(aa - offsets[i-1])
                break
    print(a1)
    for (key, value) in a1.items():
        if key in offset_to_worker_num:
            s1 = list(check(value, offset_to_worker_num[key]))
            mr_s.extend(s1 + key * np.ones(shape=np.shape(s1), dtype=int))
    print('污染数据集编号： ', mr_s)
    return mr_s



# 近似均分整数m为n份，每份相差不超过1
def splitInteger(m, n):
    assert n > 0
    quotient = m / n
    remainder = m % n
    ans = [quotient] * n
    for x in range(n - 1, -1, -1):
        if remainder < 0:
            ans[x] -= 1
            remainder += 1
        elif remainder > 0:
            ans[x] += 1
            remainder -= 1
        else:
            break
    for x in range(n):
        ans[x] = math.floor(ans[x])
    return ans


def generate_circle_queue(data, target, crl_no):
    X = []
    y = []
    parts = splitInteger(worker_num, crl_no)
    if crl_no == 1:
        X.append(data)
        y.append(target)
    while crl_no >= 2:
        size = 1 / crl_no
        X_1, X_2, y_1, y_2 = train_test_split(data, target, test_size=size)
        X.append(X_2)
        y.append(y_2)
        if crl_no == 2:
            X.append(X_1)
            y.append(y_1)
        data = X_1
        target = y_1
        crl_no = crl_no - 1
    q = queue.Queue()

    for i in range(len(X)):
        q = generate_queue(X[i], y[i], parts[i], q)
    return q



def generate_queue(data, target, parts, q):
    # q = queue.Queue()
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
    print(worker_num)
    print(contaminated_node_index)
    print(mr_check(contaminated_node_index))


def manager_start(w_n, c_n_i, xx, return_dict_3, cr_n):
    global worker_num, contaminated_node_index, circle_no
    worker_num = w_n
    contaminated_node_index = c_n_i
    # 发送任务的队列:
    task_queue = queue.Queue()
    index_queue = queue.Queue()
    # 接收结果的队列:
    result_queue = queue.Queue()
    # 环数
    circle_no = cr_n

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

    r = np.load('./data/test_2_class.npz')
    X = r['data']
    y = r['target']
    # print(X.shape)
    # print(y.shape)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    tmp =generate_circle_queue(X_train, y_train, circle_no)
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
    s1 = mr_check(contaminated_node_index)
    s = real_check(result_dict)
    print('理论应检查出污染编号：')
    print(s1)
    print('实际检查出污染编号：')
    print(s)
    # for k, v in result_dict.items():
    for i in range(worker_num):
        v = result_dict[i + 1]
        # print(v.Wb1.b)
        result_W1.append(v.Wb1.W)
        result_b1.append(v.Wb1.b)
        result_W2.append(v.Wb2.W)
        result_b2.append(v.Wb2.b)
        # 备份污染后的结果
        if (i + 1) in s:
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

    # W_ = get_mean(result_W1)
    # b_ = get_mean(result_b1)
    # l = []
    # l.append(b_)
    # clf = svm.LinearSVC()
    # clf.coef_ = W_[np.newaxis, :]
    # clf.intercept_ = np.array(l)
    # clf.classes_ = np.array([0, 1])
    # score1 = clf.score(X_test, y_test)
    # print("分布式训练正确率：")
    # print(score1)

    contaminated_W_ = get_mean(contaminated_result_W1)
    contaminated_b_ = get_mean(contaminated_result_b1)
    contaminated_l = []
    contaminated_l.append(contaminated_b_)
    clf3 = svm.LinearSVC()
    clf3.coef_ = contaminated_W_[np.newaxis, :]
    clf3.intercept_ = np.array(contaminated_l)
    clf3.classes_ = np.array([0, 1])
    score3 = clf3.score(X_test, y_test)
    print("备份污染后分布式训练正确率：")
    print(score3)

    # return_dict_1[xx] = score1
    return_dict_3[xx] = score3

    exit(0)


if __name__ == '__main__':
    manager_start()
    # indexList = range(1, worker_num + 1)
    # contaminated_node_index = random.sample(indexList, 5)
    # contaminated_node_index = [16, 33, 50]
    # test()



