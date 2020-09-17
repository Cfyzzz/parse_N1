# import pandas as pd
# from sqlalchemy import create_engine
# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np
#
# from sklearn.datasets.samples_generator import make_blobs
# from matplotlib import pyplot
# from pandas import DataFrame
#
# # generate 2d classification dataset
# X, y = make_blobs(n_samples=100, centers=3, n_features=2)
# # scatter plot, dots colored by class value
# df = DataFrame(dict(x=X[:, 0], y=X[:, 1], label=y))
# colors = {0: 'red', 1: 'blue', 2: 'green'}
# fig, ax = pyplot.subplots()
# grouped = df.groupby('label')
# for key, group in grouped:
#     group.plot(ax=ax, kind='scatter', x='x', y='y', label=key, color=colors[key])
# pyplot.savefig('demo.png', bbox_inches='tight')

import pandas as pd
from sqlalchemy import create_engine
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans




database_connection = create_engine('sqlite:///realty.sqlite3')
dataframe = pd.read_sql_query('SELECT price, area, rooms, sqm FROM apartments WHERE city like "Копейск%"', database_connection)
print(dataframe.head(5))

clusterer = KMeans(8, random_state=0)
clusterer.fit(dataframe)

dataframe['cluster'] = clusterer.predict(dataframe)

ax = dataframe.plot(x='price', y='cluster', kind='scatter')
fig = ax.get_figure()


fig.savefig('demo2.png', bbox_inches='tight')


