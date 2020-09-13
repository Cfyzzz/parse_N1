import pandas as pd
from sqlalchemy import create_engine
from matplotlib import pyplot
import statsmodels.api as sm



set_price = 100000000

database_connection = create_engine('sqlite:///realty.sqlite3')
dataframe = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Копе%" AND price <= {set_price}', database_connection)
dataframe2 = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Челябинск%" AND price <= {set_price}', database_connection)
dataframe3 = pd.read_sql_query(f'SELECT price, area, rooms, sqm FROM apartments WHERE city like "Екатеринбург%" AND price <= {set_price}', database_connection)
print(dataframe.head(5))


fig, ax = pyplot.subplots()


model = sm.formula.ols(formula='price ~ area', data=dataframe3)
res = model.fit()
dataframe3.assign(fit=res.fittedvalues).plot(x='area', y='fit', ax=ax, label='fit Екатеринбург')

model = sm.formula.ols(formula='price ~ area', data=dataframe2)
res = model.fit()
dataframe2.assign(fit=res.fittedvalues).plot(x='area', y='fit', ax=ax, label='fit Челябинск')

model = sm.formula.ols(formula='price ~ area', data=dataframe)
res = model.fit()
dataframe.assign(fit=res.fittedvalues).plot(x='area', y='fit', ax=ax, label='fit Копейск')

dataframe3.plot(ax=ax, x='area', y='price', kind='scatter', color='red', label='Екатеринбург')
dataframe2.plot(ax=ax, x='area', y='price', kind='scatter', color='green', label='Челябинск')
dataframe.plot(ax=ax, x='area', y='price', kind='scatter', color='blue', label='Копейск')

pyplot.savefig('demo2.png', bbox_inches='tight')
