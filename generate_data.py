from sklearn.datasets.samples_generator import make_classification

from matplotlib import pyplot

from pandas import DataFrame
import numpy as np

# generate 2d classification dataset
doc_word_mat_file = open('./generate.txt', 'wb')

X, y = make_classification(n_samples=10000, n_classes=2, n_features=5)
np.savez('./test_2_class.npz', data=X, target=y)
r = np.load('./test_2_class.npz')
print(r['data'])
print(r['target'])

# # scatter plot, dots colored by class value
#
# df = DataFrame(dict(x=X[:, 0], y=X[:, 1], label=y))
#
# colors = {0: 'red', 1: 'blue', 2: 'green'}
#
# fig, ax = pyplot.subplots()
#
# grouped = df.groupby('label')
#
# for key, group in grouped:
#
#    group.plot(ax=ax, kind='scatter', x='x', y='y', label=key, color=colors[key])
#
# pyplot.show()