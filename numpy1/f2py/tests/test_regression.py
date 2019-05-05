from __future__ import division, absolute_import, print_function

import os
import math
import pytest

import numpy1 as np
from numpy1.testing import assert_raises, assert_equal

from . import util


def _path(*a):
    return os.path.join(*((os.path.dirname(__file__),) + a))


class TestIntentInOut(util.F2PyTest):
    # Check that intent(in out) translates as intent(inout)
    sources = [_path('src', 'regression', 'inout.f90')]

    @pytest.mark.slow
    def test_inout(self):
        # non-contiguous should raise error
        x = np.arange(6, dtype=np.float32)[::2]
        assert_raises(ValueError, self.module.foo, x)

        # check values with contiguous array
        x = np.arange(3, dtype=np.float32)
        self.module.foo(x)
        assert_equal(x, [3, 1, 2])
