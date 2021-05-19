from __future__ import annotations

import dsutils
import numpy
import pandas
import math
import matplotlib.pyplot as pyplot

from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from collections.abc import Iterator
from typing import Optional


class HypoModel:
    """Armazena um modelo de cluster, facilitando o acesso as dados de distorção
    e inércia

    """
    globaldata: pandas.DataFrame = None

    @dsutils.logged
    @dsutils.timed
    def __init__(self, n_clusters: int,
                 data: Optional[pandas.DataFrame] = None) -> None:
        self.data = data
        self.n_clusters = n_clusters

        km = KMeans(n_clusters=n_clusters).fit(self.data)
        ds = cdist(self.data, km.cluster_centers_, 'euclidean')
        ds = sum(numpy.min(ds, axis=1))
        ds /= self.data.shape[0]

        self._kmeans = km
        self._inertia = km.inertia_
        self._distortion = ds
        self._bestinertia = False
        self._bestdistortion = False

    def __eq__(self, other: HypoModel) -> bool:
        return self.n_clusters == other.n_clusters

    @property
    def data(self) -> pandas.DataFrame:
        return self._data

    @data.setter
    def data(self, data: pandas.DataFrame) -> None:
        if data is not None:
            data = data.hypo.nona
            data = data.hypo.normalized
            data = data.hypo.balanced
            data = data.hypo.reduced
            data = data.hypo.instances
        else:
            data = HypoModel.globaldata

        if data is None:
            globaldata = f'{self.__class__.__qualname__}.globaldata'
            raise ValueError(f'Defina o valor de {globaldata} primeiro')

        self._data = data

    @property
    def n_clusters(self) -> int:
        return self._n_clusters

    @n_clusters.setter
    def n_clusters(self, n_clusters: int) -> None:
        self._n_clusters = n_clusters

    @property
    def kmeans(self) -> KMeans:
        return self._kmeans

    @property
    def distorcion(self) -> float:
        return self._distortion

    @property
    def inertia(self) -> float:
        return self._inertia

    @property
    def bestinertia(self) -> bool:
        return self._bestinertia

    @bestinertia.setter
    def bestinertia(self, bestinertia) -> None:
        self._bestinertia = bestinertia

    @property
    def bestdistortion(self) -> bool:
        return self._bestdistortion

    @bestdistortion.setter
    def bestdistortion(self, bestdistortion) -> None:
        self._bestdistortion = bestdistortion

    def scatter(self) -> pyplot.Figure:
        title = f'Modelo com {self.n_clusters:02} Clusters'
        dpi = 185
        dsutils.log(f'Plotando {title}')

        fig: pyplot.Figure
        ax: pyplot.Axes
        fig, ax = pyplot.subplots()
        fig.set_dpi(dpi)
        fig.set_size_inches(1024/dpi, 768/dpi)
        ax.set_xlim(self.data.X.min()-.5, self.data.X.max()+.1)
        ax.set_ylim(self.data.y.min()-.1, self.data.y.max()+.1)

        for c in range(self.n_clusters):
            data = self.data.assign(cluster=self.kmeans.labels_)
            data = data[data.cluster == c]
            label = f'Cluster {c + 1:02}'
            ax.scatter(x='X', y='y', data=data, label=label, alpha=0.8, s=15)

        ax.scatter(self.kmeans.cluster_centers_[:, 0],
                   self.kmeans.cluster_centers_[:, 1],
                   marker=dsutils.DSPlot.marker.plus_filled,
                   color=dsutils.DSPlot.color.darkgray,
                   alpha=0.8, label='Centroide')

        ax.legend(frameon=False, loc='upper left', fontsize='xx-small')

        if self.bestinertia:
            ax.set_xlabel('Melhor modelo segundo o critério: inércia',
                          fontsize='xx-small')

        if self.bestdistortion:
            if len(ax.get_xlabel()) > 0:
                label = f'{ax.get_xlabel()} e distorção'
            else:
                label = 'Melhor modelo segundo o critério: distorção'

            ax.set_xlabel(label, fontsize='xx-small')

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
        fig.tight_layout()

        return fig


class HypoModelList:

    def __init__(self, n_models: int, data: pandas.DataFrame) -> None:
        models = []
        n_models = numpy.arange(n_models) + 1
        data = data.hypo.nona
        data = data.hypo.normalized
        data = data.hypo.balanced
        data = data.hypo.reduced
        data = data.hypo.instances
        HypoModel.globaldata = data

        for n in n_models:
            models.append(HypoModel(n))

        inertia = numpy.array([m.inertia for m in models])
        distortion = numpy.array([m.distorcion for m in models])

        optimalinertia = HypoModelList.elbow(n_models, inertia)
        optimaldistortion = HypoModelList.elbow(n_models, distortion)
        print(optimalinertia, optimaldistortion)

        for model in models:
            model.bestinertia = optimalinertia == model.n_clusters
            model.bestdistortion = optimaldistortion == model.n_clusters

        self._models = models
        self._inertia = inertia
        self._distortion = distortion

    @staticmethod
    def elbow(x: numpy.array, y: numpy.array) -> int:
        x1, y1 = x[0], y[0]
        x2, y2 = x[-1], y[-1]

        num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        den = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        return x[int(numpy.argmax(num / den))]

    @property
    def models(self) -> list[HypoModel]:
        return self._models

    @property
    def inertia(self) -> numpy.array:
        return self._inertia

    @property
    def distortion(self) -> numpy.array:
        return self._distortion

    def model_inertia(self) -> KMeans:
        pass

    def model_distortion(self) -> KMeans:
        pass

    def plot(self) -> None:
        output = dsutils.datadir.join('plot_elbow.png')

        nc = len(self.models)
        x = numpy.arange(nc) + 1
        y1 = self.inertia
        y2 = self.distortion
        dpi = 185

        fig_elbow: pyplot.Figure
        axinertia: pyplot.Axes
        axdistortion: pyplot.Axes

        fig_elbow, axinertia = pyplot.subplots()
        fig_elbow.set_dpi(dpi)
        fig_elbow.set_size_inches(1024 / dpi, 768 / dpi)
        axdistortion = axinertia.twinx()

        axinertia.set_title(f'Algoritmo Elbow para {nc:02} Clusters')

        p1, = axinertia.plot(x, y1, label='inertia',
                             color=dsutils.DSPlot.color.lipstick)

        p2, = axdistortion.plot(x, y2, label='distortions',
                                color=dsutils.DSPlot.color.azure)

        axinertia.legend(handles=[p1, p2], frameon=False)

        style = dict(textcoords='axes fraction',
                     arrowprops=dict(facecolor=dsutils.DSPlot.color.gray,
                                     alpha=0.5, shrink=0.02),
                     fontsize='xx-small', alpha=0.8)

        for m in self.models:
            if m.bestinertia:
                bx = m.n_clusters
                by = m.inertia
                axinertia.annotate(f'optimal inertia ({bx}, {by:.2f})',
                                   (bx, by), xytext=(0.6, 0.2), **style)

            if m.bestdistortion:
                bx = m.n_clusters
                by = m.distorcion
                axdistortion.annotate(f'optimal distortion ({bx}, {by:.2f})',
                                      (bx, by), xytext=(0.6, 0.4), **style)

            n = m.n_clusters
            fname = dsutils.datadir.join(f'plot_model{n:02}.png')
            figcluster = m.scatter()
            figcluster.savefig(fname)

        axinertia.set_xticks(x)
        fig_elbow.tight_layout()
        fig_elbow.savefig(output)


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
                         facecolor=dsutils.DSPlot.color.grey,
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
