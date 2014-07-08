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

