import numpy
import pandas

import dsutils
import math
import matplotlib.pyplot as pyplot

from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from typing import Iterator


class HypoModel:
    """Armazena um modelo de cluster, facilitando o acesso as dados de distorção
    e inércia

    """

    def __init__(self, data: pandas.DataFrame, n_clusters: int) -> None:
        self._data = data
        self._kmeans = KMeans(n_clusters=n_clusters).fit(data)

    @property
    def kmeans(self):
        return self._kmeans

    @property
    def inertia(self):
        return self._

    @property
    def distorcion(self):
        data = self._data.to_numpy()
        distortion = cdist(data, self.kmeans.cluster_centers_, 'euclidean')
        distortion = sum(numpy.min(distortion, axis=1))
        distortion /= data.shape[0]


class Hypothyroid:

    def __init__(self, maxclusters: int = 12) -> None:
        csvfile = dsutils.datadir.join('hypothyroid.csv')
        self._df = pandas.read_csv(csvfile, na_values='?')
        # df = df.hypo.nona.hypo.normalized.hypo.balanced
        # df = df.normalized
        # df = df.balanced.reduced.instances.df

        maxclusters = min(maxclusters, self._df.shape[0])
        self._modeldata = self.load_model(maxclusters, self._df)

    @staticmethod
    @dsutils.logged
    @dsutils.timed
    def load_model(maxclusters: int,
                   data: pandas.DataFrame) -> pandas.DataFrame:
        model = {}
        maxclusters = numpy.arange(maxclusters) + 1

        for n in maxclusters:
            dsutils.log(f'Gerando modelo para {n} cluster(s)')
            kmeans = KMeans(n_clusters=n).fit(data)
            inertia = kmeans.inertia_

            distortion = cdist(data, kmeans.cluster_centers_, 'euclidean')
            distortion = sum(numpy.min(distortion, axis=1))
            distortion /= data.shape[0]

            model[n] = {
                'model': kmeans,
                'inertia': inertia,
                'distortion': distortion
            }

        iner = numpy.array([v['inertia'] for _, v in model.items()])
        dist = numpy.array([v['distortion'] for _, v in model.items()])

        model = pandas.DataFrame(model).T

        n = Hypothyroid.elbow(maxclusters, iner)
        n = maxclusters[n]
        model['best_inertia'] = False
        model['best_inertia'].iat[n] = True

        n = Hypothyroid.elbow(maxclusters, dist)
        n = maxclusters[n]
        model['best_distortion'] = False
        model['best_distortion'].iat[n] = True

        return model

    @staticmethod
    def elbow(x: numpy.array, y: numpy.array) -> int:
        x1, y1 = x[0], y[0]
        x2, y2 = x[-1], y[-1]

        num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        den = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        return numpy.argmax(num / den)

    @property
    def csv(self) -> pandas.DataFrame:
        return self._df

    @property
    def modeldata(self):
        return self._modeldata

    @property
    def modeldata_optimal_inertia(self) -> pandas.Series:
        return self.modeldata[self.modeldata.best_inertia]

    @property
    def modeldata_optimal_distortion(self) -> pandas.Series:
        return self.modeldata[self.modeldata.best_inertia]

    @property
    def itermodel(self) -> Iterator[tuple[KMeans, pandas.Series]]:
        for row in self.modeldata.itertuples(index=False):
            yield row.model, row

    @property
    def model_optimal_inertia(self) -> KMeans:
        return self.modeldata[self.modeldata.best_inertia].model.iloc[0]

    @property
    def model_optimal_distortion(self) -> KMeans:
        return self.modeldata[self.modeldata.best_optimal].model.iloc[0]

    def plot_elbow(self, show: bool = False) -> None:
        modeldata = self.modeldata
        modeldata_inertia = self.modeldata_optimal_inertia
        modeldata_distortion = self.modeldata_optimal_distortion

        nc = modeldata.shape[0]
        output = dsutils.datadir.join('plot_elbow.png')

        x = numpy.arange(nc) + 1
        y1 = modeldata.inertia.to_numpy()
        y2 = modeldata.distortion.to_numpy()

        fig, ax1 = pyplot.subplots()

        ax1.set_title(f'Algoritmo Elbow para {nc:02} Clusters')
        ax2 = ax1.twinx()

        p1, = ax1.plot(x, y1,
                       label='inertia',
                       color=dsutils.DSPlot.color.blue1)

        p2, = ax2.plot(x, y2,
                       label='distortions',
                       color=dsutils.DSPlot.color.purple1)

        pyplot.legend(handles=[p1, p2], frameon=False)

        style = dict(textcoords='axes fraction',
                     arrowprops=dict(
                         facecolor=dsutils.DSPlot.color.black,
                         alpha=0.5, shrink=0.02),
                     fontsize='xx-small', alpha=0.7)

        bx = modeldata_inertia.index[0]
        by = modeldata_inertia.inertia.iloc[0]
        ax1.annotate(f'optimal inertia ({bx}, {by:.2f})', (bx, by),
                     xytext=(0.6, 0.2), **style)

        bx = modeldata_distortion.index[0]
        by = modeldata_distortion.distortion.iloc[0]
        ax2.annotate(f'optimal distortion ({bx}, {by:.2f})', (bx, by),
                     xytext=(0.6, 0.4), **style)

        pyplot.xticks(x)
        fig.tight_layout()
        pyplot.savefig(output)

        if show:
            pyplot.show()

    @dsutils.logged
    @dsutils.timed
    def plot_models(self, show: bool = False):
        df = self.csv

        for model, info in self.itermodel:
            nc = model.cluster_centers_.shape[0]
            df['cluster'] = model.labels_
            output = dsutils.datadir.join(f'plot_model{nc:02}.png')
            title = f'Modelo com {nc:02} Clusters'
            dsutils.log(f'Plotando {title}')

            pyplot.xlim(df.X.min() - 1., df.X.max() + 1.)
            for c in range(nc):
                pyplot.scatter(x='X', y='y',
                               data=df[df.cluster == c],
                               label=f'Cluster {c+1:02}',
                               alpha=0.7, s=15)

            pyplot.scatter(model.cluster_centers_[:, 0],
                           model.cluster_centers_[:, 1],
                           marker=dsutils.DSPlot.marker.plus_filled,
                           color=dsutils.DSPlot.color.black,
                           alpha=0.7, label='Centroide')

            pyplot.legend(frameon=False, loc='lower left', fontsize='xx-small')
            pyplot.xticks([])
            pyplot.yticks([])
            pyplot.title(title)
            if info.best_inertia:
                pyplot.xlabel('Escolhido como o melhor modelo utilizando '
                              'algoritmo Elbow nos valores das inércias',
                              fontsize='xx-small')
            pyplot.savefig(output)
            if show:
                pyplot.show()
            pyplot.clf()
