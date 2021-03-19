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

from pyinkscape import Template, PieChart
from pyinkscape.charts import show_locs

# ------------------------------------------------------------------------------
# Draw a sample pie chart
# ------------------------------------------------------------------------------

t2 = Template().load('templates/canvas.svg')
g2 = t2.group('Layer 1')  # Search by layer name, can also try: .group_by_id('layerManual')
pie = PieChart(g2, center=(200, 200), radius=(150, 150))
pie.slide(23, 2, 12, 43, 9, 11)
pie.render()  # render pie chart
g2.new_text("Pie chart, with cream!!!", center=(200, 370), width=200, height=200)
show_locs(pie, g2)
t2.render('output/piedemo.svg')

print("Done!")
