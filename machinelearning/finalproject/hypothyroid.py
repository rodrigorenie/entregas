import pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn.preprocessing
import sklearn.metrics
import sklearn.linear_model

from scipy.spatial.distance import cdist
from dsutils import DataDir
from sklearn.cluster import KMeans

from typing import Any, Iterable, Tuple


class Hypothyroid:

    def __init__(self, csvfile: str = 'hypothyroid.csv') -> None:
        df: pandas.DataFrame = pd.read_csv(DataDir.join(csvfile), na_values='?',
                         keep_default_na=True)
        df.rocket.classcols = ['Class']
        df = df.rocket.nona.normalized.instances.df
        inertia = []
        distortions = []
        # for n in range(1, 11):
        #     model = KMeans(n_clusters=n)
        #     model.fit(df)
        #     print(model.inertia_)
        #     print(df.shape, len(df))
        #     inertia.append(model.inertia_)
        #     distortions.append(
        #         sum(
        #             np.min(
        #                 cdist(np.array(df),
        #                       model.cluster_centers_,
        #                       'euclidean'),
        #                 axis=1)
        #         ) / df.shape[0]
        #     )
        #
        # fig, ax1 = plt.subplots()
        # ax1.set_xlabel('n clusters')
        # ax1.set_ylabel('inertia')
        # ax1.plot(list(range(1, 11)), inertia)
        #
        # ax2 = ax1.twinx()
        # ax2.set_ylabel('distortions')
        # ax2.plot(list(range(1, 11)), distortions)
        #
        # fig.tight_layout()
        # plt.show()

        model = KMeans(n_clusters=6)
        predict = model.fit_predict(df)
        labels = np.unique(predict)
        # print(df.info())
        # print(df.head())
        # print(model.cluster_centers_)
        # print(model.cluster_centers_[:, 0])
        # print(model.cluster_centers_[:, 1])
        # plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1])
        # plt.show()

        from sklearn.decomposition import PCA

        # df = pd.DataFrame(np.random.rand(100, 6))
        df = pd.DataFrame(PCA(n_components=2).fit_transform(df),
                          columns=['x', 'y'])
        model = KMeans(n_clusters=3).fit(df)
        print(model.labels_)

        # df = pd.DataFrame(np.random.rand(10, 2), columns=["x", "y"])
        # print(df[df.cluster == 0])
        df['cluster'] = model.labels_

        # df = pd.DataFrame(reduced_data, columns=['A', 'B'])
        # df['cluster'] = km.labels_

        # print(df[cluster == 'A'])
        plt.scatter(df[df.cluster == 0]['x'], df[df.cluster == 0]['y'],
                    color='red')
        plt.scatter(df[df.cluster == 1]['x'], df[df.cluster == 1]['y'],
                    color='blue')
        plt.scatter(df[df.cluster == 2]['x'], df[df.cluster == 2]['y'],
                    color='green')
        plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1],
                    color='black', s=80)
        plt.show()

