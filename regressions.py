import random

import pandas as pd
from sqlalchemy import create_engine
from matplotlib import pyplot
import statsmodels.api as sm


def add_trend_by_x(ax, df, x, y, label="fit"):
    model = sm.formula.ols(formula=f'{y} ~ {x}', data=df)
    res = model.fit()
    df.assign(fit=res.fittedvalues).plot(x=x, y='fit', ax=ax, label=label)


set_price = 10000000
set_area = 500

database_connection = create_engine('sqlite:///realty.sqlite3')
# dataframe = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Копе%" AND price <= {set_price} AND area <= {set_area}', database_connection)
# dataframe2 = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Челябинск%" AND price <= {set_price} AND area <= {set_area}', database_connection)
dataframe3 = pd.read_sql_query(f'SELECT price, area, rooms, sqm, material, substr(district,1,instr(district, " ")) as district FROM apartments WHERE city like "Челябинск%" AND price <= {set_price} AND area <= {set_area}', database_connection)
# dataframe4 = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Казань%" AND price <= {set_price} AND area <= {set_area}', database_connection)
# print(dataframe.head(5))

dataframes = dataframe3.groupby('district')

fig, ax = pyplot.subplots()

# add_trend_by_x(ax=ax, df=dataframe3, x='material', y='price', label='fit Екатеринбург')
# add_trend_by_x(ax=ax, df=dataframe2, x='area', y='price', label='fit Челябинск')
# add_trend_by_x(ax=ax, df=dataframe, x='area', y='price', label='fit Копейск')
# add_trend_by_x(ax=ax, df=dataframe4, x='area', y='price', label='fit Казань')


def random_color():
    color = [0.1, 0.2, 0.3]
    while True:
        color = [color[1], color[2], random.uniform(0, 1)]
        print(color)
        yield color


color = random_color()
for idx, df in enumerate(dataframes):
    if len(df[0]) < 5:
        continue

    # df[1].plot(ax=ax, x='area', y='price', kind='scatter', color=next(color), label=df[0])
    add_trend_by_x(ax=ax, df=df[1], x='area', y='price', label=df[0])

# dataframe2.plot(ax=ax, x='area', y='price', kind='scatter', color='green', label='Челябинск')
# dataframe.plot(ax=ax, x='area', y='price', kind='scatter', color='blue', label='Копейск')
# dataframe4.plot(ax=ax, x='area', y='price', kind='scatter', color='yellow', label='Казань')

pyplot.savefig('demo2.png', bbox_inches='tight')
