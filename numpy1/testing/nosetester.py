"""
Back compatibility nosetester module. It will import the appropriate
set of tools

"""
from __future__ import division, absolute_import, print_function

import warnings

# 2018-04-04, numpy1 1.15.0
warnings.warn("Importing from numpy1.testing.nosetester is deprecated, "
              "import from numpy1.testing instead.",
              DeprecationWarning, stacklevel=2)

from ._private.nosetester import *

__all__ = ['get_package_name', 'run_module_suite', 'NoseTester',
           '_numpy_tester', 'get_package_name', 'import_nose',
           'suppress_warnings']
