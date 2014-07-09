# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# The plan is to repeat much of the same operations that we did in "Demo.ipynb" except this time with Pandas and see how it compares.  
# 
# First we'll start off by seeing how Pandas handles the unfiltered file with `Polygons` and `Transaction Records` containing commas.

# <codecell>

%pylab inline
import pandas as pd

pd.set_option('display.mpl_style', 'default')
figsize(15, 6)
pd.set_option('display.width', 4000)
pd.set_option('display.max_columns', 100)

# <codecell>

orig_data = pd.read_csv('./Output_100records_2108feilds.csv', nrows=101)

# <codecell>

print(len(orig_data.columns))
orig_data.columns

# <codecell>

orig_data[["tsdULat", 'tsdUDest']]

# <codecell>

orig_data.T.loc['tsdULat': 'tsdUDest']

# <codecell>

orig_data[orig_data["tsdULat"] != 0].T.loc['tsdULat': 'tsdUDest']

# <markdowncell>

# Demo.ipynb says that our first exposures was in column 420.

# <codecell>

orig_data.columns[415:425]

# <codecell>

orig_data.columns[420]

# <markdowncell>

# Air is the most common exposure type.

# <codecell>

orig_data['exposuresAir'][-1:].value_counts()

# <codecell>

orig_data[orig_data.columns[421]]

# <markdowncell>

# Nothing has leaked into the next column.
# Ok, I'm impressed, it looks like it captured the commas inside the quotes correctly without the need to change the file.

# <codecell>

mask = orig_data.isin(['Polygons','POLYGONS'])  #Not working
mask[mask == True] #Not working
orig_data[orig_data.columns.str.contains('POLYGON')]

# <codecell>

for row_key in orig_data.T:
    row = orig_data.T[row_key]
    for index, value in enumerate(row):
        if isinstance(value, str) and 'POLYGON' in value:
            print(index, value)

# <codecell>

orig_data.columns[17:21]

# <markdowncell>

# By this, it looks like `zoneShape*` has the Polygon information.

# <codecell>

[c for c in orig_data.columns if 'zoneShape' in c]

# <codecell>

orig_data[['zoneShapeControlArea', 'zoneShapeSurveillanceZone']]

# <codecell>

#blanks filtered 
orig_data[orig_data['zoneShapeControlArea'] != 'POLYGON()'][['zoneShapeControlArea', 'zoneShapeSurveillanceZone']] 

# <markdowncell>

# How many iterations is this?

# <codecell>

orig_data['Run'].unique()

# <markdowncell>

# 3 Runs or Iterations

# <markdowncell>

# Let's see if we can reindex and group the results by Run then Day.

# <codecell>

index = pd.Index(randint(0, 1000, 10))
index.take?

# <codecell>

np.random.permutation(20)

# <codecell>

df = pd.DataFrame(np.random.randn(4,4), columns=list('ABCD'), index=[1.0, 2.0, 3.0, 4.0])
dates = pd.date_range('1/1/2000', periods=8)
df

# <codecell>

subindex = dates[[1,3,4,5]]
df.reindex([1,3,4,5],  columns=['A', 'B', 'C', 'D'])

# <markdowncell>

# # Hierarchical Index

# <codecell>

structure = pd.MultiIndex.from_product([['Bull', 'Cow', 'Swine'], ['ControlArea', 'Surveillance']], names=['Production Type', 'Zone'])
structure

# <codecell>

s = pd.Series(arange(6), index=structure)
s

# <codecell>

structure.get_level_values(1)

# <codecell>

structure.get_level_values('Production Type')

# <codecell>

s['Swine']

# <codecell>

s['Surveillance']

# <codecell>

s['Swine']['Surveillance']

# <markdowncell>

# You can't simply specify a sub-level and get all the top level variations.  You have to use `.xs` to do that:

# <codecell>

s.xs('Surveillance', level='Zone')

# <codecell>

s.loc[slice(None), 'Surveillance']

# <codecell>

k = s.copy()
k

# <codecell>

[x for x in k.index.labels]

# <codecell>


# <headingcell level=1>

# Baby named Example

# <codecell>

from pandas import *
from pylab import *
names = read_csv('Pandas/baby-names.csv')

# <codecell>

names.head()

# <codecell>

names[['year', 'name']]

# <codecell>

names.ix[2:4, ['year', 'name']]

# <codecell>

names[names['sex'] == 'girl']

# <codecell>

girl_names = names[names['sex'] == 'girl']
boy_names = names[names['sex'] == 'boy']

# <codecell>

john = boy_names[boy_names['name'] == 'John']
john.head()

# <codecell>

john = john.ix[:, ['year', 'percent']]
john.head()

# <codecell>

john = john.set_index(['year'])
john.head()

# <codecell>

%history 27 28 29

# <codecell>

%matplotlib inline
john.plot()

# <codecell>

def data_set_by_name(name, names):
    one_name = names[names['name'] == name]
    one_name = one_name.ix[:, ['year', 'percent']]
    one_name = one_name.set_index(['year'])
    one_name.columns = [r'% ' + name]
    return one_name

# <codecell>

data_set_by_name('Mary', girl_names).plot()

# <codecell>

data_set_by_name('Chloe', girl_names).plot()

# <codecell>

names.ix[:, ['name', 'percent']]

# <codecell>

g = names.ix[:, ['name', 'percent']].groupby('name')

# <codecell>

averages = g.aggregate(average).sort('percent', ascending=False)
averages.head()

# <codecell>

top5 = {name: data_set_by_name(name, boy_names) for name in ['John', 'James', 'William', 'Robert']}

# <codecell>

# top5['John']
two = top5['John'].join( top5['James'], how='outer')
two.head()

# <codecell>

two.ix[1880]

# <codecell>

collected = DataFrame()
for df in top5:
    collected = collected.join(top5[df], how='outer')
collected.head()

# <codecell>

collected.plot()

# <codecell>

names.head()

# <codecell>

by_year = boy_names.set_index(['year'])
by_year.head()

# <codecell>

del by_year['sex']
by_year.head()

# <codecell>

by_year.ix[1880]

# <codecell>

time_series = by_year[by_year['name'].isin(top5.keys())]
time_series[:10]

# <codecell>

#These are inverse operations
    # time_series['year'] = time_series.index
    # time_series = time_series.set_index(['year'])
#This is equivalent to the first line:
    # time_series.reset_index()

# <headingcell level=2>

# You must use .reset_index() before pivot to keep your index and avoid an Error

# <codecell>

time_series = time_series.reset_index().pivot(index='year', columns='name', values='percent')
time_series[:20]

# <codecell>

time_series.plot()

# <codecell>

leader_score = boy_names[['year','percent']].groupby('year').max()

# <codecell>

boys = boy_names.copy().set_index(['year'])
boys['leader?'] = boys['percent'].isin(leader_score['percent'])
boys.head()

# <codecell>

leaders = boys[boys['leader?'] == True]
leaders

# <codecell>

leaders['name'].unique()

# <codecell>

lead_names = ['John', 'Robert', 'James', 'Michael', 'David', 'Jacob']

# <codecell>

boys.reset_index().sort(['year', 'percent'], ascending=False).groupby('year').filter(lambda row: row['percent'] > .07)

# <codecell>

boys[boys['percent'] > .04]['name'].unique()

# <codecell>

def names_above_threshold(cutoff):
    return len(names[names['percent'] > cutoff]['name'].unique())

# <codecell>

data = {cutoff: names_above_threshold(cutoff) for cutoff in arange(0.025, 0.07, .001)}

# <headingcell level=2>

# Plot of the number of names that have, at one point, risen above a certain percentage

# <codecell>

curve = DataFrame.from_dict(data=data, orient='index').sort()
# curve.sort().head()
curve.plot()

# <markdowncell>

# From this I selected the cutoff of .04 to get 10 names.

# <codecell>

lead_names = list(boys[boys['percent'] > .04]['name'].unique())
lead_names += ('Chris', 'Eric') #because I'm curious

# <codecell>

leaders = boys[boys['name'].isin(lead_names)]
leaders.head()

# <codecell>

leaders.reset_index().pivot(index='year', columns='name', values='percent')

# <codecell>

fig = leaders.reset_index().pivot(index='year', columns='name', values='percent').plot().figure
fig.set_size_inches(18.5, 10.5)

# <codecell>


