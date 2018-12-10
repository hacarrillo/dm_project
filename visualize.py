import numpy as np
import argparse
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from PIL import Image
import imageio
import os
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist
import csv
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import math
from sklearn.decomposition import PCA

csv_file = 'smallUserListGenres_Clustering.csv'

with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    my_data = list(reader)

my_data = np.array(my_data)
my_data = my_data[1:,:]

s = np.shape(my_data)
num_choose = int(s[0]*1.)
idx = np.random.choice(s[0],num_choose)

vectors = my_data[idx,2:]
print(np.shape(vectors))
vectors = vectors.astype(np.float64)

watched = vectors[:,0::2]
scored = vectors[:,1::2]

average = np.zeros_like(scored)

s = np.shape(watched)

for i in range(s[0]):
	for j in range(s[1]):
		if watched[i,j] == 0:
			average[i,j] = 0
		else:
			average[i,j] = int(scored[i,j]/watched[i,j])

pca = PCA(n_components=2)
result = pca.fit_transform(vectors)
# print("generating coordinates")
# result = TSNE(n_components=2, random_state=0).fit_transform(vectors)
# print("finished generating coordinates")

print(np.shape(result))
plt.scatter(x=result[:,0], y=result[:,1])
plt.show()