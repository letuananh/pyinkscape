#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Test script for pyInkscape
Latest version can be found at https://github.com/letuananh/pyinkscape

:copyright: (c) 2021 Le Tuan Anh <tuananh.ke@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
import unittest
import logging
import warnings
from pathlib import Path
from pyinkscape import Canvas


# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

TEST_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
TEST_CANVAS = TEST_DIR / 'data/canvas-0.92.4.svg'
TEST_GRAPHIC = TEST_DIR / 'data/graphic.svg'


def getLogger():
    return logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Test cases
# ------------------------------------------------------------------------------

class TestTemplate(unittest.TestCase):

    def test_load_inkscape_file(self):
        t = Canvas(TEST_CANVAS)
        self.assertTrue(t)

    def test_new_blank_template(self):
        t = Canvas()
        self.assertTrue(t)

    def test_empty_template(self):
        t = Canvas(filepath=None)
        self.assertTrue(t)

    def test_static_load_function(self):
        with self.assertWarnsRegex(
                DeprecationWarning,
                r'load\(\) is deprecated [a-z ]+, use Canvas constructor instead\.') as cm:
            t = Canvas.load(TEST_CANVAS)

    def test_read_svg_properties(self):
        t = Canvas()
        # test reading size info
        _properties = (t.width, t.height, t.units, t.viewBox.to_tuple(), t.scale)
        _expected = (210.0, 297.0, 'mm', (0.0, 0.0, 840.0, 1188.0), 4.0)
        self.assertEqual(_properties, _expected)
        # test reading version info
        self.assertEqual((t.version, t.inkscape_version), ('1.1', '1.0.1 (3bc2e813f5, 2020-09-07)'))
        # assert that 'new.svg' is in the generated SVG code
        # test docname (by default, docname is 'blank.svg')
        self.assertEqual(t.docname, 'blank.svg')
        t.docname = 'new.svg'
        self.assertEqual(t.docname, 'new.svg')
        self.assertIn('sodipodi:docname="new.svg"', str(t))


class TestSelectingObject(unittest.TestCase):

    def test_layer_search(self):
        c = Canvas()
        layers = c.layers()
        self.assertEqual(len(layers), 1)
        l = layers[0]  # the first layer
        l1 = c.layer('Layer 1')
        self.assertIsNotNone(l1)
        l2 = c.layer_by_id('layer1')
        self.assertIsNotNone(l2)
        self.assertNotEqual(l1, l2)
        self.assertEqual((l1.ID, l1.label, l1.elem), (l2.ID, l2.label, l2.elem))

    def test_group_search(self):
        c = Canvas(TEST_GRAPHIC)
        groups = c.groups()
        self.assertEqual(len(groups), 6)
        _expected_groups = {('complex shape 2', 'g886'), ('Layer 2', 'layer2'),
                            (None, 'g855'), ('Layer 1', 'layerManual'),
                            (None, 'g841'), ('complex shape 1', 'g837')}
        self.assertEqual({(x.label, x.ID) for x in groups}, _expected_groups)
        g1a = c.group('Layer 1')
        self.assertEqual(g1a.label, 'Layer 1')
        g1b = c.group('Layer 1', layer_only=True)
        self.assertEqual(g1b.label, 'Layer 1')
        # look for a group that is layer by ID
        g2a = c.group_by_id("layer2")
        self.assertIsNotNone(g2a)
        g2b = c.group_by_id("layer2", layer_only=True)
        self.assertIsNotNone(g2b)
        # look for a group without a label (i.e. label is implied by ID)
        g3a = c.group('g855')
        self.assertIsNotNone(g3a)
        self.assertIsNone(g3a.label)


class TestSVGManipulation(unittest.TestCase):

    def test_draw(self):
        c = Canvas()
        l = c.layers()[0]
        l.text("Hello World", (50, 50))
        l.circle((50, 50), 100)
        _xml_code = str(c)
        self.assertIn("__pyinkscape_text_", _xml_code)
        self.assertIn("__pyinkscape_circle_", _xml_code)

    def test_remove_group(self):
        c = Canvas()
        l = c.layer('Layer 1')
        o = l.elem.find('..')
        print(l, o)


# -------------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
