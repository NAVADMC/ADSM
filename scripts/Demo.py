# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# 100 Rows Demo

# <markdowncell>

# Some notes on what I'm doing

# <markdowncell>

# List:
# * first
# * second

# <codecell>

import re
raw_file = open('Output_100records_2108feilds.csv')
raw_file

# <codecell>

text = raw_file.read()

# <codecell>

text = re.sub(r'\([^)]*\)', '', text)

# <codecell>

text = re.sub(r'"?POLYGON["\)\(\s]*', '', text)

# <codecell>

text

# <codecell>

lines = text.split('\n')
lines[1]

# <codecell>

headers = lines[0].split(',')
headers

# <codecell>

def extract_exposure_record(line):
    new_text = line
    for match in re.finditer('"[\d\-\>,]*"', line):
        record = match.group(0)
        preceeding_text = line[0: match.start()]
        column_number = preceeding_text.count(',')
        better_pipes = re.sub(',', '|', record)
        new_text = re.sub(record, better_pipes, new_text)  # delete the record from the raw text
        
    return new_text

# <codecell>

extract_exposure_record(lines[50])

# <codecell>

old_lines = lines
lines = [extract_exposure_record(line) for line in old_lines]
lines[50:52]

# <codecell>

[index for index, line in enumerate(lines) if line.count('"') > 4]  # This show line numbers with more than one exposure record

# <codecell>

def matching_headers(prefix, exclude=None):
    matches = [h for h in headers if h.startswith(prefix)]
    if exclude is not None:
        matches = [m for m in matches if exclude not in m]
    print('\n'.join(matches))
    print('Total:', len(matches))

# <codecell>

matching_headers('exposure')

# <codecell>

lines = lines[1:]  # remove headers from lines

# <codecell>

data = [row.split(',') for row in lines]  # split column on comma
data[1]

# <codecell>

for d in data[:3]:
    print(len(d))

# <codecell>

prefix = 'exposure'
matches = [(col_index, name) for col_index, name in enumerate(headers) if name.startswith(prefix)]
for column, name in matches:
    print()
    print()
    print(name)
    for row in data:
        if len(row) > column and row[column]:
            print(','.join([row[0], row[1], row[column]]))

# <codecell>


# <codecell>

for line in text:
    print(a,b,x)
    print()
[line for line in text]

# <codecell>

'words here there'.split()
# ','.join('words    here   \n  there'.split())

# <codecell>

'words    here   \n  there'.count('e')

# <codecell>

[word for word in ['words', 'hereadadada', 'there'] if len(word) > 5]

# <markdowncell>

# ###Python Libraries
# * CSV reader -> might handle some cases like commas inside quotes
# * Pandas -> Square Data Manipulation = Tables with named row and columns
#  * Table style math -> conjugate columns, summations, exlusions

# <codecell>

import csv
lines = '''"AAA", "BBB", "Test, Test", "CCC"
           "111", "222, 333", "XXX", "YYY, ZZZ"'''.splitlines()
for l in  csv.reader(lines, quotechar='"', delimiter=',',
                     quoting=csv.QUOTE_ALL, skipinitialspace=True):
    print(l)

# <codecell>


# <codecell>

csv.list_dialects()

# <codecell>


with open('clean_100row.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in data:
        spamwriter.writerow(row)

# <codecell>


