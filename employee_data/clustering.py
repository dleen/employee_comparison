import parse_corpus
import numpy as np
import pylab as pl

import simply_measured as sm

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

tfidf, labels, feat_names = parse_corpus.get_data()
labels = np.array(labels)

print labels


n_samples, n_features = tfidf.shape

# est = KMeans(init='k-means++', n_clusters=3)
pca = PCA(n_components=2, whiten=True)
reduced_data = pca.fit_transform(tfidf.toarray())

kmeans = KMeans(init='k-means++', n_clusters=2)
kmeans.fit(reduced_data)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = 0.02     # point in the mesh [x_min, m_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will asign a color to each
x_min, x_max = reduced_data[:, 0].min() - 0.1, reduced_data[:, 0].max() + 0.1
y_min, y_max = reduced_data[:, 1].min() - 0.1, reduced_data[:, 1].max() + 0.1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
pl.figure(1)
pl.clf()
pl.imshow(Z, interpolation='nearest',
          extent=(xx.min(), xx.max(), yy.min(), yy.max()),
          cmap=pl.cm.Paired,
          aspect='auto', origin='lower')

pl.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
pl.scatter(centroids[:, 0], centroids[:, 1],
           marker='x', s=169, linewidths=3,
           color='w', zorder=10)

pl.plot(reduced_data[labels == 0, 0],
        reduced_data[labels == 0, 1], 'r.', markersize=10)
pl.text(reduced_data[0, 0], reduced_data[0, 1], 'David Leen')

pl.plot(reduced_data[labels == 1, 0],
        reduced_data[labels == 1, 1], 'b.', markersize=5)
pl.plot(reduced_data[labels == 2, 0],
        reduced_data[labels == 2, 1], 'g.', markersize=5)
pl.plot(reduced_data[labels == 3, 0],
        reduced_data[labels == 3, 1], 'c.', markersize=5)
for i, n in enumerate(sm.simply_measured_people, start=1):
    print i, n, reduced_data[i, 0], reduced_data[i, 1]
    pl.text(reduced_data[i, 0], reduced_data[i, 1], n)

pl.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
         'Centroids are marked with white cross')
pl.xlim(x_min, x_max)
pl.ylim(y_min, y_max)
pl.xticks(())
pl.yticks(())
pl.show()
