# from nltk.cluster.kmeans import KMeansClusterer
# NUM_CLUSTERS = <choose a value>
# data = <sparse matrix that you would normally give to scikit>.toarray()

# kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
# assigned_clusters = kclusterer.cluster(data, assign_clusters=True)
import numpy
from nltk.cluster import KMeansClusterer, euclidean_distance

vectors = [numpy.array(f) for f in [[2, 1], [1, 3], [4, 7], [6, 7]]]
means = [[4, 3], [5, 5]]

clusterer = KMeansClusterer(2, euclidean_distance, initial_means=means)
clusters = clusterer.cluster(vectors, True, trace=True)

print('Clustered:', vectors)
print('As:', clusters)
print('Means:', clusterer.means())
print()
