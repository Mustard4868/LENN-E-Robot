"""
This is the package for the robot module.

:author:  Niels Baarsma
:license: The Unlicense

"""

__title__ = 'robot'
__author__ = 'Niels Baarsma'
__license__ = 'The Unlicense'
__version__ = '0.1.0'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .movement import *
from .sensor import *
from .statemachine import *