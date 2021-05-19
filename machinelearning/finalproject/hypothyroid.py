from __future__ import annotations

import dsutils
import numpy
import pandas
import math
import matplotlib.pyplot as pyplot

from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from typing import Optional


class HypoModel:
    """Armazena um modelo de cluster, facilitando o acesso as dados de distorção
    e inércia

    """
    globaldata: pandas.DataFrame = None

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

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
        fig.tight_layout()

        return fig


class HypoModelList:

    def __init__(self, n_models: int, data: pandas.DataFrame) -> None:
        models = []
        newdata = data.hypo.nona
        newdata = newdata.hypo.normalized
        newdata = newdata.hypo.balanced
        newdata = newdata.hypo.reduced
        newdata = newdata.hypo.instances
        HypoModel.globaldata = newdata

        for n in range(1, n_models + 1):
            models.append(HypoModel(n))

        self._data = data
        self._models = models
        self._inertias = numpy.array([m.inertia for m in models])
        self._distortions = numpy.array([m.distorcion for m in models])
        self._model_inertia = self.elbow_inertia()
        self._model_distortion = self.elbow_inertia()

    @staticmethod
    def elbow(x: numpy.array, y: numpy.array) -> int:
        x1, y1 = x[0], y[0]
        x2, y2 = x[-1], y[-1]

        num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        den = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        return int(numpy.argmax(num / den))

    def elbow_inertia(self) -> HypoModel:
        x = numpy.arange(len(self.models)) + 1
        y = numpy.array([m.inertia for m in self.models])
        p = HypoModelList.elbow(x, y)
        return self.models[p]

    def elbow_distortion(self) -> HypoModel:
        x = numpy.arange(len(self.models)) + 1
        y = numpy.array([m.distorcion for m in self.models])
        p = HypoModelList.elbow(x, y)
        return self.models[p]

    @property
    def data(self) -> pandas.DataFrame:
        return self._data

    @property
    def models(self) -> list[HypoModel]:
        return self._models

    @property
    def inertias(self) -> numpy.array:
        return self._inertias

    @property
    def distortions(self) -> numpy.array:
        return self._distortions

    @property
    def model_inertia(self) -> HypoModel:
        return self._model_inertia

    @property
    def model_distortion(self) -> HypoModel:
        return self._model_distortion

    def plot(self) -> None:
        output = dsutils.datadir.join('plot_elbow.png')

        nc = len(self.models)
        x = numpy.arange(nc) + 1
        y1 = self.inertias
        y2 = self.distortions
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

        for model in self.models:
            n = model.n_clusters
            fname = dsutils.datadir.join(f'plot_model{n:02}.png')
            figcluster = model.scatter()
            axcluster, = figcluster.axes

            if model == self.model_inertia:
                bx = model.n_clusters
                by = model.inertia
                axinertia.annotate(f'optimal inertia ({bx}, {by:.2f})',
                                   (bx, by), xytext=(0.6, 0.2), **style)
                axcluster.set_xlabel('Melhor modelo segundo o critério: '
                                     'inércia', fontsize='xx-small')

            if model == self.model_distortion:
                bx = model.n_clusters
                by = model.distorcion
                axdistortion.annotate(f'optimal distortion ({bx}, {by:.2f})',
                                      (bx, by), xytext=(0.6, 0.4), **style)
                if len(axcluster.get_xlabel()) > 0:
                    label = f'{axcluster.get_xlabel()} e distorção'
                else:
                    label = 'Melhor modelo segundo o critério: distorção'
                axcluster.set_xlabel(label, fontsize='xx-small')

            figcluster.savefig(fname)

        axinertia.set_xticks(x)
        fig_elbow.tight_layout()
        fig_elbow.savefig(output)


class Hypothyroid(HypoModelList):

    @dsutils.logged
    @dsutils.timed
    def __init__(self, n_models: Optional[int] = 16) -> None:
        csvfile = dsutils.datadir.join('hypothyroid.csv')
        df = pandas.read_csv(csvfile, na_values='?')
        super().__init__(n_models, df)
