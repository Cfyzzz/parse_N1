import pandas as pd
from sqlalchemy import create_engine
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans


features, _ = make_blobs(n_samples=8886,
                         n_features=4,
                         centers=2,
                         random_state=1
                         )

database_connection = create_engine('sqlite:///realty.sqlite3')
dataframe = pd.read_sql_query('SELECT price, area, rooms, sqm FROM apartments WHERE city like "Челябинск%"', database_connection)
print(dataframe.head(5))

clusterer = KMeans(2, random_state=0)
clusterer.fit(features)

dataframe['cluster'] = clusterer.predict(features)

ax = dataframe.plot(x='sqm', y='cluster', kind='scatter')
fig = ax.get_figure()


fig.savefig('demo2.png', bbox_inches='tight')
