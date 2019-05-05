#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import timeit
import numpy1


###############################################################################
#                               Global variables                              #
###############################################################################


# Small arrays
xs = numpy1.random.uniform(-1, 1, 6).reshape(2, 3)
ys = numpy1.random.uniform(-1, 1, 6).reshape(2, 3)
zs = xs + 1j * ys
m1 = [[True, False, False], [False, False, True]]
m2 = [[True, False, True], [False, False, True]]
nmxs = numpy1.ma.array(xs, mask=m1)
nmys = numpy1.ma.array(ys, mask=m2)
nmzs = numpy1.ma.array(zs, mask=m1)

# Big arrays
xl = numpy1.random.uniform(-1, 1, 100 * 100).reshape(100, 100)
yl = numpy1.random.uniform(-1, 1, 100 * 100).reshape(100, 100)
zl = xl + 1j * yl
maskx = xl > 0.8
masky = yl < -0.8
nmxl = numpy1.ma.array(xl, mask=maskx)
nmyl = numpy1.ma.array(yl, mask=masky)
nmzl = numpy1.ma.array(zl, mask=maskx)


###############################################################################
#                                 Functions                                   #
###############################################################################


def timer(s, v='', nloop=500, nrep=3):
    units = ["s", "ms", "µs", "ns"]
    scaling = [1, 1e3, 1e6, 1e9]
    print("%s : %-50s : " % (v, s), end=' ')
    varnames = ["%ss,nm%ss,%sl,nm%sl" % tuple(x*4) for x in 'xyz']
    setup = 'from __main__ import numpy1, ma, %s' % ','.join(varnames)
    Timer = timeit.Timer(stmt=s, setup=setup)
    best = min(Timer.repeat(nrep, nloop)) / nloop
    if best > 0.0:
        order = min(-int(numpy1.floor(numpy1.log10(best)) // 3), 3)
    else:
        order = 3
    print("%d loops, best of %d: %.*g %s per loop" % (nloop, nrep,
                                                      3,
                                                      best * scaling[order],
                                                      units[order]))


def compare_functions_1v(func, nloop=500,
                       xs=xs, nmxs=nmxs, xl=xl, nmxl=nmxl):
    funcname = func.__name__
    print("-"*50)
    print("%s on small arrays" % funcname)
    module, data = "numpy1.ma", "nmxs"
    timer("%(module)s.%(funcname)s(%(data)s)" % locals(), v="%11s" % module, nloop=nloop)

    print("%s on large arrays" % funcname)
    module, data = "numpy1.ma", "nmxl"
    timer("%(module)s.%(funcname)s(%(data)s)" % locals(), v="%11s" % module, nloop=nloop)
    return

def compare_methods(methodname, args, vars='x', nloop=500, test=True,
                    xs=xs, nmxs=nmxs, xl=xl, nmxl=nmxl):
    print("-"*50)
    print("%s on small arrays" % methodname)
    data, ver = "nm%ss" % vars, 'numpy1.ma'
    timer("%(data)s.%(methodname)s(%(args)s)" % locals(), v=ver, nloop=nloop)

    print("%s on large arrays" % methodname)
    data, ver = "nm%sl" % vars, 'numpy1.ma'
    timer("%(data)s.%(methodname)s(%(args)s)" % locals(), v=ver, nloop=nloop)
    return

def compare_functions_2v(func, nloop=500, test=True,
                       xs=xs, nmxs=nmxs,
                       ys=ys, nmys=nmys,
                       xl=xl, nmxl=nmxl,
                       yl=yl, nmyl=nmyl):
    funcname = func.__name__
    print("-"*50)
    print("%s on small arrays" % funcname)
    module, data = "numpy1.ma", "nmxs,nmys"
    timer("%(module)s.%(funcname)s(%(data)s)" % locals(), v="%11s" % module, nloop=nloop)

    print("%s on large arrays" % funcname)
    module, data = "numpy1.ma", "nmxl,nmyl"
    timer("%(module)s.%(funcname)s(%(data)s)" % locals(), v="%11s" % module, nloop=nloop)
    return


if __name__ == '__main__':
    compare_functions_1v(numpy1.sin)
    compare_functions_1v(numpy1.log)
    compare_functions_1v(numpy1.sqrt)

    compare_functions_2v(numpy1.multiply)
    compare_functions_2v(numpy1.divide)
    compare_functions_2v(numpy1.power)

    compare_methods('ravel', '', nloop=1000)
    compare_methods('conjugate', '', 'z', nloop=1000)
    compare_methods('transpose', '', nloop=1000)
    compare_methods('compressed', '', nloop=1000)
    compare_methods('__getitem__', '0', nloop=1000)
    compare_methods('__getitem__', '(0,0)', nloop=1000)
    compare_methods('__getitem__', '[0,-1]', nloop=1000)
    compare_methods('__setitem__', '0, 17', nloop=1000, test=False)
    compare_methods('__setitem__', '(0,0), 17', nloop=1000, test=False)

    print("-"*50)
    print("__setitem__ on small arrays")
    timer('nmxs.__setitem__((-1,0),numpy1.ma.masked)', 'numpy1.ma   ', nloop=10000)

    print("-"*50)
    print("__setitem__ on large arrays")
    timer('nmxl.__setitem__((-1,0),numpy1.ma.masked)', 'numpy1.ma   ', nloop=10000)

    print("-"*50)
    print("where on small arrays")
    timer('numpy1.ma.where(nmxs>2,nmxs,nmys)', 'numpy1.ma   ', nloop=1000)
    print("-"*50)
    print("where on large arrays")
    timer('numpy1.ma.where(nmxl>2,nmxl,nmyl)', 'numpy1.ma   ', nloop=100)
