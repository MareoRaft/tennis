#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram

# players: handedness, age, ranking,
# ATPsite: height, weight, % service pts won,
# view-source:www.atpworldtour.com/en/players/sandor-noszaly/n112/player-stats
# serve speed in https://raw.githubusercontent.com/JeffSackmann/tennis_slam_pointbypoint/master/2012-frenchopen-points.csv
# cluster players by weight

# height is centimeters and weight is kilograms
data = np.genfromtxt("data/player-hw.csv", names=True, dtype=float, delimiter=",")
print(len(data))
print(len(data.dtype.names))
data_array = data.view((np.float, len(data.dtype.names)))
data_array = data_array.transpose()
print(data_array)

data_dist = pdist(data_array)
data_link = linkage(data_dist) # compute the linkage

dendrogram(data_link, labels=data.dtype.names)
plt.xlabel('Players')
plt.ylabel('Distance')
plt.suptitle('Player clustering', fontweight='bold', fontsize=14);
plt.show()

