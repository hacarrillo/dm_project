from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn import decomposition
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt

with open("mediumUserListGenres_Clustering.csv") as f:
    ncols = len(f.readline().split(','))
data_file = open("smallUserListGenres_Clustering.csv")
data = np.loadtxt(data_file, delimiter=',', skiprows=1, usecols=range(10, ncols))  # noqa
x = list(data)
X = np.array(x).astype("int")
num_rows = len(X)
k_clusters = int(math.sqrt(num_rows)/2)
watched = X[:, 0::2]
scored = X[:, 1::2]
average = np.zeros_like(scored)
s = np.shape(watched)

for i in range(s[0]):
    for j in range(s[1]):
        if watched[i, j] == 0:
            average[i, j] = 0
        else:
            average[i, j] = int(scored[i, j]/watched[i, j])
X = average
pca = decomposition.PCA(n_components=2)
pca.fit(X)
X = pca.transform(X)
clustering = KMeans(n_clusters=k_clusters, random_state=0).fit(X)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = clustering.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(X[:, 0], X[:, 1], 'k.', markersize=2, alpha=0.35)
# Plot the centroids as a white X
centroids = clustering.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
          'Centroids are marked with white cross\n'
          'Number of clusters:%d ' % k_clusters)
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()

# clustering = DBSCAN(eps=0.5, min_samples=5).fit(X)
# print(set(clustering.labels_))
# core_samples_mask = np.zeros_like(clustering.labels_, dtype=bool)
# core_samples_mask[clustering.core_sample_indices_] = True
# labels = clustering.labels_
# unique_labels = set(labels)
# colors = [plt.cm.Spectral(each)
#           for each in np.linspace(0, 1, len(unique_labels))]
# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise.
#         col = [0, 0, 0, 1]

#     class_member_mask = (labels == k)

#     xy = X[class_member_mask & core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
#              markeredgecolor='k', markersize=5)

#     xy = X[class_member_mask & ~core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
#              markeredgecolor='k', markersize=1)
# plt.show()
