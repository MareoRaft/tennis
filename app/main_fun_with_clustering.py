#!/usr/bin/env python2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

data = np.genfromtxt("data/data_clustering.tab",names=True,usecols=tuple(range(1,30)),dtype=float, delimiter="\t")
print len(data)
print len(data.dtype.names)
data_array = data.view((np.float, len(data.dtype.names)))
data_array = data_array.transpose()
print data_array

data_dist = pdist(data_array)
data_link = linkage(data_dist) # compute the linkage

dendrogram(data_link, labels=data.dtype.names)
plt.xlabel('Samples')
plt.ylabel('Distance')
plt.suptitle('Samples clustering', fontweight='bold', fontsize=14);
# plt.show()

