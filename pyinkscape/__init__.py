from . import __version__ as version_info
from .__version__ import __author__, __email__, __copyright__, __maintainer__
from .__version__ import __credits__, __license__, __description__, __url__
from .__version__ import __version_major__, __version_long__, __version__, __status__
from .inkscape import Canvas, Point, Dimension, Style
from .charts import PieChart
from .styles import DEFAULT_LINESTYLE, STYLE_FPNAME, BLIND_COLORS


__all__ = ['Canvas', 'PieChart', 'Point', 'Style',
           'DEFAULT_LINESTYLE', 'STYLE_FPNAME', 'BLIND_COLORS']
