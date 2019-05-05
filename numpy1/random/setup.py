from __future__ import division, print_function

from os.path import join, split, dirname
import os
import sys
from distutils.dep_util import newer
from distutils.msvccompiler import get_build_version as get_msvc_build_version

def needs_mingw_ftime_workaround():
    # We need the mingw workaround for _ftime if the msvc runtime version is
    # 7.1 or above and we build with mingw ...
    # ... but we can't easily detect compiler version outside distutils command
    # context, so we will need to detect in randomkit whether we build with gcc
    msver = get_msvc_build_version()
    if msver and msver >= 8:
        return True

    return False

def configuration(parent_package='',top_path=None):
    from numpy1.distutils.misc_util import Configuration, get_mathlibs
    config = Configuration('random', parent_package, top_path)

    def generate_libraries(ext, build_dir):
        config_cmd = config.get_config_cmd()
        libs = get_mathlibs()
        if sys.platform == 'win32':
            libs.append('Advapi32')
        ext.libraries.extend(libs)
        return None

    # enable unix large file support on 32 bit systems
    # (64 bit off_t, lseek -> lseek64 etc.)
    if sys.platform[:3] == "aix":
        defs = [('_LARGE_FILES', None)]
    else:
        defs = [('_FILE_OFFSET_BITS', '64'),
                ('_LARGEFILE_SOURCE', '1'),
                ('_LARGEFILE64_SOURCE', '1')]
    if needs_mingw_ftime_workaround():
        defs.append(("NPY_NEEDS_MINGW_TIME_WORKAROUND", None))
    # fix for 0.26 < cython < 0.29 and perhaps 0.28.5
    # see https://github.com/cython/cython/issues/2494
    defs.append(('CYTHON_SMALL_CODE', ''))

    libs = []
    # Configure mtrand
    config.add_extension('mtrand',
                         sources=[join('mtrand', x) for x in
                                  ['mtrand.c', 'randomkit.c', 'initarray.c',
                                   'distributions.c']]+[generate_libraries],
                         libraries=libs,
                         depends=[join('mtrand', '*.h'),
                                  join('mtrand', '*.pyx'),
                                  join('mtrand', '*.pxi'),],
                         define_macros=defs,
                         )

    config.add_data_files(('.', join('mtrand', 'randomkit.h')))
    config.add_data_dir('tests')

    return config


if __name__ == '__main__':
    from numpy1.distutils.core import setup
    setup(configuration=configuration)