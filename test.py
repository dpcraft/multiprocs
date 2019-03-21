# # encoding:utf8
# # [[ 0.14731262 -0.41763159 -0.54708438 -0.00599309  1.08360124]]
# # [-0.16949917]
import numpy as np
import random
import os
np.set_printoptions(suppress=True)
# from sklearn import svm
# np.set_printoptions(threshold=np.inf)
# r = np.load('./data/test_2_class.npz')
# X = r['data']
# y = r['target']
# W = [[0.14731262], [-0.41763159], [-0.54708438], [-0.00599309],  [1.08360124]]
# tmp = np.dot(X[:30, :], W)
# b = -0.16949917 * np.ones(shape=tmp.shape)
# clf = svm.LinearSVC()
# clf.coef_ = np.array([[0.14731262, -0.41763159, -0.54708438, -0.00599309, 1.08360124]])
# clf.intercept_ = [-0.16949917]
# clf.classes_ = np.array([0, 1])
# # clf.predict([[0.8976399,0.49182796, -1.10221125, -0.95746198, 0.72237154]])
# predict = tmp + b
# print(predict.reshape(1, -1))
# print(clf.predict(X[:30, :]))
# print(y[:30])
# print(clf.predict(X[:30, :]) - y[:30])
# print(clf.score(X[:30, :], y[:30]))
#
#

# # 每一列求平均
# print(np.mean([[1, 2], [3, 4]], axis=0))
# # 每一行求平均
# print(np.mean([[1, 2], [3, 4]], axis=1))
# # 所有平均
# print(np.mean([[1, 2], [3, 4]]))

# W1 = [[ 0.13310845, -0.4118735,  -0.51969297,  0.00676181,  1.04594874]]
# b1 = [-0.16580334]
# W2 = [[ 0.17599961, -0.4757767,  -0.63658587, -0.06345159,  1.24972353]]
# b2 = [-0.20681303]
# W3 = [[ 0.16829812, -0.43535224, -0.59432333, -0.0047103,   1.15707183]]
# b3 = [-0.15481265]
# W = W1 + W2 + W3
# print(W)
# print('#' * 50)
# print(np.mean(W, axis=0))




# W = [[0.13075517, -0.40775788, -0.51283161,  0.05077295,  1.03358807],
#  [0.13074877, - 0.40776333, - 0.51282518,  0.05077947,  1.0335867]]
#  # [0.13074933, - 0.40776387, - 0.51282648,  0.05077858,  1.03358876],
#  # [0.1307478, - 0.40776273, - 0.51282316,  0.05077688,  1.03358372]]
# print(np.mean(W, axis=0))
# print(np.var(W, axis=0))
# for i in range(5):
#     print(float(i + 1))

# 输出不一致的数据集编号
# no = 20
# a = [1, 11, 12, 20]


# def check(a):
#     s = set()
#     for i in a:
#         if ((i % no) + 1) not in a:
#             s.add((i % no) + 1)
#         if((i - 2 + no) % no + 1) not in a:
#             print(i)
#             s.add(i)
#     print(s)
#     return s
# for i in s:
#     a.remove(i)
# print(a)
# len = 10
# indexList = range(1, len + 1)
# randomIndex = random.sample(indexList, 5)
# print(indexList)
# print(randomIndex)
#encoding:utf-8
# import multiprocessing
#
#
# def proc1(pipe):
#     print('hello')
#     pipe.send("hello")
#     # print("proc 1 : ", pipe.recv())
#
#
# def proc2(pipe):
#     print("proc 2 : ", pipe.recv())
#     # pipe.send("hello ,too")
#
#
# # 创建一个管道　这个管道是双向的
# pipe = multiprocessing.Pipe()
#
# # pipe[0]　表示管道的一端，pipe[1] 表示管道的另外一端
# # 对ｐｉｐｅ的某一端调用ｓｅｎｄ方法来传送对象，在另外一端使用ｒｅｃｖ来接收
#
# p2 = multiprocessing.Process(target=proc2, args=(pipe[1],))
# p2.start()
# for i in range(5):
#     multiprocessing.Process(target=proc1, args=(pipe[0],)).start()
#
#
# p2.join()
# coding:utf-8


# os.system('nohup /home/sdnfv/dpcraft/skenv/bin/python3.4 -u ./sk_manager.py > ./log/sk_manager.log 2>&1 &')
# print('manager is started')
# print('*' * 50)
# time.sleep(1)


# def start_worker():
#     os.system('/home/sdnfv/dpcraft/skenv/bin/python3.4 -u ./sk_worker.py > ./log/sk_worker_%d.log 2>&1' % i)


# def start_manager(name):
#     print('%s is starting' % name)
#     os.system('/home/sdnfv/dpcraft/skenv/bin/python3.4 -u ./sk_manager.py > ./log/sk_manager.log 2>&1')


# p = Process(target=start_manager, args=('manager',))


# import numpy as np
# import matplotlib.pyplot as plt
#
#
# x1 = [20, 33, 51, 79, 101, 121, 132, 145, 162, 182, 203, 219, 232, 243, 256, 270, 287, 310, 325]
# y1 = [49, 48, 48, 48, 48, 87, 106, 123, 155, 191, 233, 261, 278, 284, 297, 307, 341, 319, 341]
# x2 = [31, 52, 73, 92, 101, 112, 126, 140, 153, 175, 186, 196, 215, 230, 240, 270, 288, 300]
# y2 = [48, 48, 48, 48, 49, 89, 162, 237, 302, 378, 443, 472, 522, 597, 628, 661, 690, 702]
# x3 = [30, 50, 70, 90, 105, 114, 128, 137, 147, 159, 170, 180, 190, 200, 210, 230, 243, 259, 284, 297, 311]
# y3 = [48, 48, 48, 48, 66, 173, 351, 472, 586, 712, 804, 899, 994, 1094, 1198, 1360, 1458, 1578, 1734, 1797, 1892]
# # x = np.arange(20, 350)
# l1 = plt.plot(x1, y1, 'r--', label='Distributed pollution free')
# l2 = plt.plot(x2, y2, 'g--', label='Distributed no backup')
# l3 = plt.plot(x3, y3, 'b--', label='Distributed backup')
# plt.plot(x1, y1, 'ro-', x2, y2, 'g+-', x3, y3, 'b^-')
# plt.title('The Result in Three Conditions')
# plt.xlabel('Number of contaminated nodes')
# plt.ylabel('score')
# plt.legend()
# plt.show()
# [0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334, 0.8973333333333334]
# [0.8973333333333334, 0.8974, 0.8976000000000001, 0.8978333333333334, 0.8973666666666666, 0.8973000000000001, 0.8972666666666667, 0.8977333333333334, 0.8972333333333333, 0.8970666666666668, 0.8969666666666667, 0.8975333333333333, 0.8971000000000002, 0.8979666666666667, 0.8971333333333333, 0.8963666666666666, 0.8965, 0.8963999999999999, 0.8974, 0.8967666666666668, 0.8950333333333333, 0.8919666666666668, 0.8939666666666668, 0.8851666666666667, 0.8129, 0.47673333333333334, 0.3164666666666667, 0.11426666666666667, 0.10583333333333333, 0.10576666666666665, 0.1045, 0.10436666666666668, 0.10300000000000001, 0.10346666666666667, 0.1024, 0.10286666666666666, 0.10270000000000001, 0.10329999999999999, 0.1022, 0.10303333333333334, 0.10263333333333333, 0.10303333333333334, 0.10200000000000001, 0.10246666666666666, 0.10236666666666668, 0.1024, 0.10246666666666666, 0.1026, 0.10203333333333334, 0.10253333333333334, 0.10266666666666666]
# [0.8973333333333334, 0.8973333333333334, 0.8973000000000001, 0.8973333333333334, 0.8973666666666666, 0.8972000000000001, 0.8973000000000001, 0.8973000000000001, 0.8975, 0.8975, 0.8972333333333335, 0.8978000000000002, 0.8974333333333334, 0.8977333333333333, 0.8975, 0.8978000000000002, 0.8974333333333334, 0.8974666666666667, 0.8974666666666666, 0.8975666666666665, 0.8975666666666665, 0.8975666666666667, 0.8974333333333334, 0.8973333333333334, 0.8979666666666667, 0.8968999999999999, 0.8970666666666668, 0.8975000000000002, 0.8969333333333334, 0.8970333333333335, 0.8977666666666668, 0.8955, 0.8831666666666667, 0.8914666666666667, 0.7874, 0.5094333333333333, 0.35073333333333334, 0.1986, 0.10666666666666666, 0.10400000000000001, 0.10356666666666667, 0.10310000000000001, 0.10253333333333334, 0.10313333333333333, 0.1024, 0.10283333333333333, 0.10269999999999999, 0.10233333333333335, 0.10196666666666668, 0.10256666666666667, 0.10266666666666666]
#
#
# def splitInteger(m, n):
#     assert n > 0
#     quotient = m / n
#     remainder = m % n
#     if remainder > 0:
#         return [quotient] * (n - remainder) + [quotient + 1] * remainder
#     if remainder < 0:
#         return [quotient - 1] * -remainder + [quotient] * (n + remainder)
#     return [quotient] * n
import math

# r = np.load('./data/test_2_class.npz')
# X = r['data']
# y = r['target']
# # X = X + 100
# # print(X[:1])
# W1 = np.mat([1.02930144, 0.02947777, 0.00666236, -0.03248445, 0.10220627, 0.09301269,
#      0.04804846, -0.38417057, -0.07516978, -0.03204406, -0.31839528, 0.07806351,
#      -0.01323791, 0.05328783, -0.01024464, -0.06558974, -0.0323086, -0.02217908,
#      0.03799191, -0.05189142])
#
#
#
# def poisoning(X):
#     W = np.array([[1.81854289, 0.67689115, 0.49769656, 0.27501146, 0.16297571, 1.07459496
#                       , 0.40320964, 0.06145882, -0.0334066, 0.06819986, 0.48113072, 0.81664863
#                       , 0.47775273, 0.61443478, 0.48544784, 0.15116699, 0.84786672, 0.19863598
#                       , 0.90899323, 0.33328904]])
#     b = [-0.11907137]
#     p = np.dot(X[:10], W.T) + b
#     print(p)
#     p[p < 0] = 0
#     p[p > 0] = 1
#     print(p)
#     pp = p.astype(np.int)
#     return np.squeeze(pp)
# print(y[:10])
# pp[pp < 0] = 0
# pp[pp > 0] = 1
# print(pp[:1])
# print(type(X))
# print(W + np.random.random(size=W.shape))
# X = np.multiply(X, X)
# print(X)
#

# import copy
# from trans import Trans
#
# def poisoning(target):
#     # pp = [random.randrange(10) for i in range(target.shape[0])]
#     # return np.squeeze(pp)
#     return 9 - target
#
#
# def contaminate_data(d):
#     # print(d.target.shape)
#     # d.target = np.ones(shape=d.target.shape) - d.target
#     # d.target = 1 - d.target
#     # d.data = np.random.random(size=d.data.shape) * 10
#     d.target = poisoning(d.target)
#     d.data = d.data * d.data
#     return d
# client_d = []
# X = Trans(data=np.array([[1, 2, 3]]), target=np.array([1]))
# X1 = Trans(data=np.array([[4, 5, 6]]), target=np.array([0]))
# client_d.append(X)
# client_d.append(X1)
# client_d_contaminated = copy.deepcopy(client_d)
#
# for i in client_d_contaminated:
#     print('污染前：')
#     print(i.data)
#     print(i.target)
#     i = contaminate_data(i)
#     # print('污染后：')
#     # print(i.target)
# for i in client_d_contaminated:
#     print('污染后：')
#     print(i.data)
#     print(i.target)
# # print('污染后的数据训练结果：')
target = np.array([[1, 2, 3],[1,2,3]])
# pp = [random.randrange(10) for i in range(target.shape[0])]
print(np.random.random(target.shape) * 100)
