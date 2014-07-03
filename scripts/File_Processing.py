# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

xml_file = open('../workspace/Population_Ireland.xml', 'r')

# <codecell>

lines = [l for l in xml_file.readlines()]
lines[:10]

# <codecell>

import re
[line for line in lines if re.search('production-type', line)]

# <codecell>


