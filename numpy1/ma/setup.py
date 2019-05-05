#!/usr/bin/env python
from __future__ import division, print_function

def configuration(parent_package='',top_path=None):
    from numpy1.distutils.misc_util import Configuration
    config = Configuration('ma', parent_package, top_path)
    config.add_data_dir('tests')
    return config

if __name__ == "__main__":
    from numpy1.distutils.core import setup
    config = configuration(top_path='').todict()
    setup(**config)
