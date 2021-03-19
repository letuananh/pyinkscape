Getting Started
===============

pyInkscape is a tiny library that helps reading and editing `Inkscape`_ SVG graphic files.

.. _Inkscape: https://inkscape.org/

Installation
------------
pyInkscape is available on PyPI and can be installed using `pip`.

.. code-block:: bash

   pip install --user pyinkscape

To make sure that pyinkscape has been installed properly, try:

.. code-block:: bash

   python -c "import pyinkscape; print(pyinkscape.__version__)"
   0.1a2

Or inside Python:

>>> import pyinkscape
>>> pyinkscape.__version__
'0.1a2'

First pyInkscape script
-----------------------

This script create an empty canvas (i.e. Inkscape page), finds the layer with the name "Layer 1",
and then write "Hello World" onto that layer.
The result is then written into the file `hello.svg`.

>>> from pyinkscape import Canvas
>>> t = Canvas()
>>> l = t.layer('Layer 1')
>>> l.text("Hello World", center=(100, 100))
>>> t2.render('hello.svg')
