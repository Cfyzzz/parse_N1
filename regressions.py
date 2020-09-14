import pandas as pd
from sqlalchemy import create_engine
from matplotlib import pyplot
import statsmodels.api as sm


def add_trend_by_x(ax, df, x, y, label="fit"):
    model = sm.formula.ols(formula=f'{y} ~ {x}', data=df)
    res = model.fit()
    df.assign(fit=res.fittedvalues).plot(x=x, y='fit', ax=ax, label=label)


set_price = 10000000
set_area = 150

database_connection = create_engine('sqlite:///realty.sqlite3')
dataframe = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Копе%" AND price <= {set_price} AND area <= {set_area}', database_connection)
dataframe2 = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Челябинск%" AND price <= {set_price} AND area <= {set_area}', database_connection)
dataframe3 = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Екатеринбург%" AND price <= {set_price} AND area <= {set_area}', database_connection)
dataframe4 = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Казань%" AND price <= {set_price} AND area <= {set_area}', database_connection)
print(dataframe.head(5))


fig, ax = pyplot.subplots()

add_trend_by_x(ax=ax, df=dataframe3, x='area', y='price', label='fit Екатеринбург')
add_trend_by_x(ax=ax, df=dataframe2, x='area', y='price', label='fit Челябинск')
add_trend_by_x(ax=ax, df=dataframe, x='area', y='price', label='fit Копейск')
add_trend_by_x(ax=ax, df=dataframe4, x='area', y='price', label='fit Казань')

dataframe3.plot(ax=ax, x='area', y='price', kind='scatter', color='red', label='Екатеринбург')
dataframe2.plot(ax=ax, x='area', y='price', kind='scatter', color='green', label='Челябинск')
dataframe.plot(ax=ax, x='area', y='price', kind='scatter', color='blue', label='Копейск')
dataframe4.plot(ax=ax, x='area', y='price', kind='scatter', color='yellow', label='Казань')

pyplot.savefig('demo2.png', bbox_inches='tight')
