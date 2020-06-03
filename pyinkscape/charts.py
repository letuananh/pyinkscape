#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Helper functions to draw charts using Inkscape SVG

Latest version can be found at https://github.com/letuananh/pyinkscape

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

import itertools

from .inkscape import Point
from .inkscape import BLIND_COLORS
from .inkscape import Style

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

STYLE_SLIDE = Style(fill= "#0066CC", fill_opacity='1', fill_rule='nonzero', stroke_width='0px', stroke='none')
STYLE_REDDOT = Style(display='inline', opacity='0.98799995', fill='#FF0000', stroke='#e00000', stroke_width='0.52916664', stroke_miterlimit='4', stroke_dasharray='none', stroke_opacity='1')

# ------------------------------------------------------------------------------
# Piechart
# ------------------------------------------------------------------------------

class PieSlide:
    def __init__(self, start, percent, pie):
        self.start = Point.ensure(start)
        self.pie = pie
        self.percent = percent
        self.update()

    def update(self, previous=0):
        self.target = Point.rotate_percent(self.start, self.pie.center, self.percent + previous)  # destination to draw an arc to
        return self.target

    def path(self, previous=0):
        _target = self.update(previous=previous)
        large = 1 if self.percent > 50 else 0  # large_arc_flag
        _path = f"M {self.start.x} {self.start.y} A {self.pie.radius.x} {self.pie.radius.y}, {self.pie.rotate}, {large}, 1, {_target.x} {_target.y} L {self.pie.center.x} {self.pie.center.y} Z"
        return _path


class PieChart:
    def __init__(self, group, center, radius, slides=None, colors=BLIND_COLORS, rotate=0):
        self.group = group
        self.center = Point.ensure(center)
        self.radius = Point.ensure(radius)
        self.slides = list(slides) if slides else []
        self.colors = colors
        self.rotate = 0

    def slide(self, *percents):
        _slides = []
        for percent in percents:
            if percent <= 0:
                continue
            _slide = PieSlide((0, 0), percent, self)
            self.slides.append(_slide)
            _slides.append(_slides)
        return _slides

    def paths(self):
        _sx, _sy = self.center.x, self.center.y - self.radius.y
        _paths = []
        # _accu = 0
        for slide in self.slides:
            slide.start.x = _sx
            slide.start.y = _sy
            _path = slide.path()  # (previous=_accu)
            _paths.append(_path)
            _sx = slide.target.x  # move point to the next
            _sy = slide.target.y
            # _accu += slide.percent  # accumulation
        return _paths

    def render_slide(self, path, color, **kwargs):
        return self.group.path(path, style=STYLE_SLIDE.clone(fill=color), **kwargs)

    def render(self, colors=None, id_prefix="piechart"):
        _colors = colors if colors else self.colors
        if len(self.slides) == 1 and self.slides[0].percent == 100:
            # draw a circle
            self.group.circle(self.center, self.radius.x, style=STYLE_SLIDE.clone(fill=_colors[0]), id_prefix=f"{id_prefix}_circle")
        else:
            for idx, (path, color) in enumerate(zip(self.paths(), itertools.cycle(_colors)), start=1):
                self.render_slide(path, color, id_prefix=f"{id_prefix}_slide{idx}")


def show_locs(pie, group, radius=3):
    ''' Highlight important points of a pie chart '''
    green = STYLE_REDDOT.clone(fill='#00FF00')
    for slide in pie.slides:
        group.circle(slide.start, radius, style=green)
        group.circle(slide.target, radius, style=green)
    # draw the center point
    group.circle(pie.center, radius, style=STYLE_REDDOT)

