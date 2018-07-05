# # encoding:utf8
# # [[ 0.14731262 -0.41763159 -0.54708438 -0.00599309  1.08360124]]
# # [-0.16949917]
import numpy as np
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

W1 = [[ 0.13310845, -0.4118735,  -0.51969297,  0.00676181,  1.04594874]]
b1 = [-0.16580334]
W2 = [[ 0.17599961, -0.4757767,  -0.63658587, -0.06345159,  1.24972353]]
b2 = [-0.20681303]
W3 = [[ 0.16829812, -0.43535224, -0.59432333, -0.0047103,   1.15707183]]
b3 = [-0.15481265]
W = W1 + W2 + W3
print(W)
print('#' * 50)
print(np.mean(W, axis=0))
