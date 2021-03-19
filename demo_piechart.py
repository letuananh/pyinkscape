#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Demo pie chart drawing using pyInkscape

Latest version can be found at https://github.com/letuananh

@author: Le Tuan Anh <tuananh.ke@gmail.com>
@license: MIT
'''

# Copyright (c) 2017, Le Tuan Anh <tuananh.ke@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

########################################################################

import pyinkscape
from pyinkscape import Canvas, PieChart
from pyinkscape.charts import show_locs


# ------------------------------------------------------------------------------
# Development information
# ------------------------------------------------------------------------------
print("-" * 60)
print("pyInkscape demo pie chart code")
print("-" * 60)
print(f"lxml available: {pyinkscape.inkscape._LXML_AVAILABLE}")
print(f"chirptext available: {pyinkscape.inkscape._CHIRPTEXT_AVAILABLE}")
print()

# ------------------------------------------------------------------------------
# Draw a sample pie chart
# ------------------------------------------------------------------------------
# 1. Open an Inkscape SVG file
t2 = Canvas('templates/canvas.svg')  # or use Template() to create an empty canvas
# find a group by name
g2 = t2.group('Layer 1')  # Search by layer name, can also try: .group_by_id('layerManual')

# 2. Drawing 
# Create a pie chart object
pie = PieChart(g2, center=(200, 200), radius=(150, 150))
pie.slide(23, 2, 12, 43, 9, 11)
# Draw the pie chart
pie.render()
# Draw a text
g2.text("Pie chart, with cream!!!", center=(200, 370), width=200, height=200)
# Show locations on pie chart
show_locs(pie, g2)

# 3. Generate output SVG file
# Add overwrite=True to bypass pyInkscape overwrite protection
t2.render('output/piedemo.svg', overwrite=True)
