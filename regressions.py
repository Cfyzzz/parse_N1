import pandas as pd
from sqlalchemy import create_engine
from matplotlib import pyplot


database_connection = create_engine('sqlite:///realty.sqlite3')
dataframe = pd.read_sql_query('SELECT price, area, rooms, sqm FROM apartments WHERE city like "Копе%"', database_connection)
dataframe2 = pd.read_sql_query('SELECT price, area, rooms, sqm FROM apartments WHERE city like "Челябинск%"', database_connection)
dataframe3 = pd.read_sql_query('SELECT price, area, rooms, sqm FROM apartments WHERE city like "Екатеринбург%"', database_connection)
print(dataframe.head(5))

fig, ax = pyplot.subplots()

dataframe3.plot(ax=ax, x='area', y='price', kind='scatter', color='red', label='Екатеринбург')
dataframe2.plot(ax=ax, x='area', y='price', kind='scatter', color='green', label='Челябинск')
dataframe.plot(ax=ax, x='area', y='price', kind='scatter', color='blue', label='Копейск')

pyplot.savefig('demo2.png', bbox_inches='tight')
