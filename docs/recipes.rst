Recipes for Common Usecases
===========================

These are common usecases of pyInkscape.

Load an existing Inkscape file
------------------------------

>>> c = Canvas('/home/user/Pictures/my_file.svg')

Finding layers
--------------

Layers can be searched by either names or IDs.

.. code-block:: python

   c = Canvas('/home/user/Pictures/my_file.svg')
   # get all existing layers
   layers = c.layers()
   # get a layer by name
   layer1 = c.layer("Layer 1")
   # get a layer by ID
   layer1 = c.layer_by_id("layer1")

Draw a text
-----------

Use the `text()` method of a `Layer` object to draw a text onto that layer.

>>> from pyInkscape import Canvas
>>> c = Canvas()
>>> l = c.layer("Layer 1")
>>> l.text("Hello World", (50, 50))
>>> c.render("output.svg")
