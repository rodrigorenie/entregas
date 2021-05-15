import numpy
import pandas
import matplotlib.pyplot as pyplot
import functools

import dsutils
import math
import sklearn.preprocessing
import sklearn.metrics
import sklearn.linear_model


from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans

from typing import Any, Iterable, Tuple, Optional





class Hypothyroid:

    def __init__(self, csvfile: Optional[str] = 'hypothyroid.csv',
                 n_clusters: int = 5) -> None:
        self._csvfile = dsutils.DataDir.join(csvfile)
        self._n_clusters = n_clusters

    @functools.cached_property
    def df(self) -> dsutils.RocketFrame:
        df = pandas.read_csv(self.csvfile, na_values='?')
        df.rocket.classcols = ['Class']
        return df.rocket.nona.normalized.balanced.reduced.instances.df

    @property
    def n_clusters(self):
        return min(self._n_clusters, self.df.shape[0])

    @property
    def csvfile(self):
        return self._csvfile

    def optimal_number_of_clusters(self, wcss):
        wcss1, wcss2 = self.distances
        x1, y1 = 1, wcss[0]
        x2, y2 = self.n_clusters, wcss[len(wcss) - 1]

        y0 = numpy.array(wcss)
        x0 = numpy.array(range(len(wcss)))+2
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        return numpy.argmax(numerator/denominator) + 2

    @functools.cached_property
    def distances(self) -> tuple[list[float],  list[float]]:
        inertia, distortion = [], []

        for n in range(1, self.n_clusters + 1):
            model = KMeans(n_clusters=n).fit(self.df)
            inertia.append(model.inertia_)
            distance = cdist(self.df, model.cluster_centers_, 'euclidean')
            distortion.append(numpy.average(distance))

        return inertia, distortion

    @functools.cached_property
    def model(self) -> KMeans:
        model = []
        for n in range(1, self.n_clusters+1):
            model.append(KMeans(n_clusters=n).fit(self.df))



    @functools.cached_property
    def distortions(self) -> list[float]:
        values = self.df.rocket.nona.normalized.reduced.instances.df.values()
        print(type(values))
        distortions = []
        for n in range(1, self._maxclusters):
            model = KMeans(n_clusters=n).fit(df)
            ine = model.inertia_
            dis = sum(
                np.min(
                    cdist(np.array(df),
                          model.cluster_centers_,
                          'euclidean'),
                    axis=1)
            ) / df.shape[0]

            print(ine, dis)
            inertia.append(ine)
            distortions.append(dis)

        fig, host = pyplot.subplots()
        host.set_xlabel('n clusters')
        x = optimal_number_of_clusters(inertia)
        y = inertia[x]
        print('clusters inertia:', x, y, sum(inertia)/len(inertia))
        p1, = host.plot(list(range(1, 11)), inertia, label='inertia',
                        color=dsutils.Colors.blue)
        # p3 = host.axvline(x, ymax=y, color=dsutils.Colors.amber, alpha=0.4,
        #              label=f'Clusters Inertia: {x}')
        p4 = host.scatter(x, y, s=30, marker='v', color=dsutils.Colors.blue,
                         label='ideal clusters by inertia')
        ax1 = host.twinx()
        x = optimal_number_of_clusters(distortions)
        y = distortions[x]
        print('clusters distortions:', x, y, )
        p2, = ax1.plot(list(range(1, 11)), distortions, label='distortions',
                       color=dsutils.Colors.green)
        # ax1.axvline(x, ymax=y, color=dsutils.Colors.purple, alpha=0.4)
        p3 = ax1.scatter(x, y, s=30, marker='v', color=dsutils.Colors.green,
                         label='ideal clusters by distortions')

        # fig.tight_layout()
        pyplot.xticks(list(range(1, 11)))
        pyplot.legend(handles=[p1, p2, p3, p4], frameon=False)
        pyplot.show()
        raise SystemExit

        # model = KMeans(n_clusters=6)
        # predict = model.fit_predict(df)
        # labels = np.unique(predict)
        # print(df.info())
        # print(df.head())
        # print(model.cluster_centers_)
        # print(model.cluster_centers_[:, 0])
        # print(model.cluster_centers_[:, 1])

        # df = pd.DataFrame(np.random.rand(100, 6))
        model = KMeans(n_clusters=6).fit(df)
        print(model.labels_)
        df['cluster'] = model.labels_
        colors = {
            0: 'red',
            1: 'green',
            2: 'blue'
        }

        # print(df[cluster == 'A'])
        # plt.scatter(df[df.cluster == 0]['X'], df[df.cluster == 0]['y'],
        #             color='red')
        pyplot.xlim(df.X.min() - 1., df.X.max() + 1.)
        for cluster in set(df.cluster):
            pyplot.scatter(x='X', y='y',
                           data=df[df.cluster == cluster],
                           label=f'Cluster {cluster}')
        pyplot.scatter(model.cluster_centers_[:, 0],
                    model.cluster_centers_[:, 1],
                       marker='P', color='black',
                       label='Centroids')
        pyplot.legend(frameon=False, loc='lower left', fontsize='xx-small')
        # plt.axis('off')
        pyplot.xticks([])
        pyplot.yticks([])
        pyplot.show()

