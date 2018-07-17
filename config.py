import random
worker_num = 10
contaminated_num = 5
contaminated_node_index = [1, 2, 3, 7, 9, 27]
indexList = range(1, worker_num + 1)
contaminated_node_index = random.sample(indexList, contaminated_num)
print(indexList)
print(contaminated_node_index)
