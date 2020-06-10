#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Helper functions to manipulate Inkscape SVG content

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

import os
import logging
import math
import warnings
from lxml import etree
from chirptext.anhxa import IDGenerator
from chirptext.cli import setup_logging

# -------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

setup_logging('logging.json', 'logs')


def getLogger():
    return logging.getLogger(__name__)


class Style:
    def __init__(self, **kwargs):
        self.attributes = {}
        self.attributes.update(kwargs)

    # alias of attributes
    @property
    def attrs(self):
        return self.attributes

    def __str__(self):
        return ";".join("{}:{}".format(k.replace('_', '-'), v) for k, v in self.attributes.items())

    def clone(self, **kwargs):
        s = Style(**self.attributes)
        s.attributes.update(kwargs)
        return s


SVG_NS = {'ns':'http://www.w3.org/2000/svg',
          'svg': 'http://www.w3.org/2000/svg',
          'inkscape': 'http://www.inkscape.org/namespaces/inkscape'}
DEFAULT_LINESTYLE = Style(display='inline', fill='none', stroke_width='0.86458332px', stroke_linecap='butt', stroke_linejoin='miter', stroke_opacity='1', stroke='#FF0000')
STYLE_FPNAME = Style(font_size='20px', font_family='sans-serif', font_style='normal', font_weight='normal', line_height='1.25', letter_spacing='0px', word_spacing='0px', fill='#000000', fill_opacity='1', stroke='none')
BLIND_COLORS = ("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")
__idgen = IDGenerator()


def new_id(prefix=None):
    if not prefix:
        prefix = '_pyinkscape_'
    return '{prefix}_{id}'.format(prefix=prefix, id=next(__idgen))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, Dimension):
            return Point(self.x + other.width, self.y + other.height)
        else:
            return Point(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        if isinstance(other, Dimension):
            return Point(self.x - other.width, self.y - other.height)
        else:
            return Point(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        if isinstance(other, Dimension):
            return Point(self.x * other.width, self.y * other.height)
        else:
            return Point(self.x * other, self.y * other)

    def __div__(self, other):
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        if isinstance(other, Dimension):
            return Point(self.x / other.width, self.y / other.height)
        else:
            return Point(self.x / other, self.y / other)

    @staticmethod
    def rotate_percent(point, center, percent):
        degrees = percent * 3.6
        getLogger().debug(f"Percent: {percent} - Degrees: {degrees}")
        return Point.rotate(point, center, degrees)

    @staticmethod
    def ensure(p):
        if isinstance(p, Point):
            return p
        else:
            return Point(*p)

    @staticmethod
    def rotate(point, center, theta):
        ''' theta is the rotating angle, in degrees '''
        point = Point.ensure(point)
        center = Point.ensure(center)
        t_rad = math.radians(theta)
        n_x = point.x - center.x  # shift center point to (0, 0)
        n_y = point.y - center.y
        getLogger().debug(f"shifted = ({n_x}, {n_y}) - theta (in radians) = {t_rad}")
        r_x = n_x * math.cos(t_rad) - n_y * math.sin(t_rad)  # rotation matrix
        r_y = n_x * math.sin(t_rad) + n_y * math.cos(t_rad)
        getLogger().debug(f"new point = ({r_x + center.x}, {r_y + center.y})")
        return Point(r_x + center.x, r_y + center.y)  # shift it back


class Dimension:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def ensure(p):
        if isinstance(p, Dimension):
            return p
        else:
            return Dimension(*p)


class Group:
    def __init__(self, elem):
        self.elem = elem
        self.ID = elem.get('id')
        self.tag = elem.tag
        self.label = elem.get('label')

    def paths(self):
        paths = self.elem.xpath('//ns:path', namespaces=SVG_NS)
        return [Path(p) for p in paths]

    def new(self, tag_name, id=None, style=None, id_prefix=None, **kwargs):
        e = etree.SubElement(self.elem, tag_name)
        if not id:
            id = new_id(prefix=id_prefix)
        e.set('id', id)
        if style:
            e.set('style', str(style))
        for k, v in kwargs.items():
            e.set(str(k), str(v))
        return e

    def line(self, from_point, to_point, style=DEFAULT_LINESTYLE, **kwargs):
        from_point = Point.ensure(from_point)
        to_point = Point.ensure(to_point)
        return self.new("line",
                        x1=from_point.x, y1=from_point.y,
                        x2=to_point.x, y2=to_point.y,
                        style=style,
                        **kwargs)

    def rect(self, topleft, size, style=DEFAULT_LINESTYLE, **kwargs):
        topleft = Point.ensure(topleft)
        size = Dimension.ensure(size)
        return self.new("rect", x=topleft.x, y=topleft.y, width=size.width, height=size.height, style=style, **kwargs)

    def path(self, path_code, id=None, style=DEFAULT_LINESTYLE, **kwargs):
        p = self.new("path", style=style, **kwargs)
        p.set('d', path_code)
        p.set('{http://www.inkscape.org/namespaces/inkscape}connector-curvature', "0")
        return Path(p)

    def circle(self, center, r, style=DEFAULT_LINESTYLE, **kwargs):
        center = Point.ensure(center)
        c = self.new("circle", style=style, **kwargs)
        c.set('cx', str(center.x))
        c.set('cy', str(center.y))
        c.set('r', str(r))
        return Circle(c)

    def text(self, text, center, width='', height='', font_size='18px', font_family="sans-serif", fill="black", text_anchor='middle', style=STYLE_FPNAME, id_prefix=None, **kwargs):
        txt = self.new('text', id_prefix=id_prefix)
        center = Point.ensure(center)
        txt.set('x', str(center.x))
        txt.set('y', str(center.y))
        txt.set('font-size', font_size)
        txt.set('font-family', font_family)
        txt.set('fill', fill)
        txt.set('text-anchor', text_anchor)
        if style:
            txt.set('style', str(style))        
        for k, v in kwargs.items():
            txt.set(k, str(v))
        txt.text = text
        return Text(txt)

    @property
    def new_path(self):
        warnings.warn("new_path() is deprecated and will be removed in near future.", DeprecationWarning, stacklevel=2)
        return self.path

    @property
    def new_circle(self):
        warnings.warn("new_circle() is deprecated and will be removed in near future.", DeprecationWarning, stacklevel=2)
        return self.circle

    @property
    def new_text(self):
        warnings.warn("new_text() is deprecated and will be removed in near future.", DeprecationWarning, stacklevel=2)
        return self.text


class Shape:
    def __init__(self, elem):
        self.elem = elem
        self.ID = elem.get('id')
        self.label = elem.get('label')


class Text(Shape):
    pass


class Circle(Shape):
    pass


class Path(Shape):
    pass


class Template:

    def __init__(self):
        self.tree = None

    def load(self, filepath, remove_blank_text=True, encoding="utf-8", **kwargs):
        with open(filepath, encoding=encoding) as infile:
            parser = etree.XMLParser(remove_blank_text=remove_blank_text, **kwargs)
            self.tree = etree.parse(infile, parser)
            self.root = self.tree.getroot()
        return self

    def to_xml_string(self, encoding="utf-8", pretty_print=True, **kwargs):
        return etree.tostring(self.root, encoding=encoding, pretty_print=pretty_print, **kwargs).decode('utf-8')

    def __str__(self):
        return self.to_xml_string()

    def groups(self):
        groups = self.root.xpath("/ns:svg/ns:g", namespaces=SVG_NS)
        return [Group(g) for g in groups]

    def group(self, name):
        groups = self.root.xpath(f"/ns:svg/ns:g[@id='{name}']", namespaces=SVG_NS)
        return Group(groups[0]) if groups else None

    def render(self, outpath, overwrite=False, encoding="utf-8"):
        if not overwrite and os.path.isfile(outpath):
            getLogger().warn(f"File {outpath} exists. SKIPPED")
        else:
            output = str(self)
            with open(outpath, mode='w', encoding=encoding) as outfile:
                outfile.write(output)
                getLogger().info("Written output to {}".format(outfile.name))

    def getText(self, id):
        elems = self.root.xpath("/ns:svg/ns:g/ns:flowRoot[@id='{id}']/ns:flowPara".format(id=id), namespaces=SVG_NS)
        if elems:
            return elems
        else:
            # try get <text> element instead of flowRoot ...
            elems = self.root.xpath("/ns:svg/ns:g/ns:text[@id='{id}']/ns:tspan".format(id=id), namespaces=SVG_NS)
            getLogger().debug(f"Found: {elems}")
            return elems
