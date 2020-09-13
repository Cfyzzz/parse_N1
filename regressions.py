import pandas as pd
from sqlalchemy import create_engine


database_connection = create_engine('sqlite:///realty.sqlite3')
dataframe = pd.read_sql_query('SELECT price, area, rooms FROM apartments WHERE city like "Челябинск%"', database_connection)
print(dataframe.head(5))


ax = dataframe.plot(x='price', y='area', kind='scatter')
fig = ax.get_figure()


fig.savefig('demo2.png', bbox_inches='tight')
