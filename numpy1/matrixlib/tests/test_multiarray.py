from __future__ import division, absolute_import, print_function

import pytest

import numpy1 as np
from numpy1.testing import assert_, assert_equal, assert_array_equal

class TestView(object):
    def test_type(self):
        x = np.array([1, 2, 3])
        assert_(isinstance(x.view(np.matrix), np.matrix))

    def test_keywords(self):
        x = np.array([(1, 2)], dtype=[('a', np.int8), ('b', np.int8)])
        # We must be specific about the endianness here:
        y = x.view(dtype='<i2', type=np.matrix)
        assert_array_equal(y, [[513]])

        assert_(isinstance(y, np.matrix))
        assert_equal(y.dtype, np.dtype('<i2'))
