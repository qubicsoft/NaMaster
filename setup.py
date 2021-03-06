#!/usr/bin/env python
import sys
from setuptools import setup, Extension

# Get numpy include directory (works across versions)
import numpy
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

if '--enable-fftw-pthreads' in sys.argv:
    sys.argv.pop(sys.argv.index('--enable-fftw-pthreads'))
    FFTW_LIBS = ['fftw3', 'fftw3_threads', 'pthread']
else:
    FFTW_LIBS = ['fftw3', 'fftw3_omp']

if '--disable-openmp' in sys.argv:
    sys.argv.pop(sys.argv.index('--disable-openmp'))
    USE_OPENMP = False
else:
    USE_OPENMP = True

libs = [
    'nmt', 'sharp', 'fftpack', 'c_utils', 'chealpix', 'cfitsio', 'gsl',
    'gslcblas', 'm'] + FFTW_LIBS

use_icc = False  # Set to True if you compiled libsharp with icc
if use_icc:
    extra = []
    if USE_OPENMP:
        libs += ['gomp', 'iomp5']
        extra += ['-openmp']
else:
    extra = ['-O4']
    if USE_OPENMP:
        libs += ['gomp']
        extra += ['-fopenmp']

_nmtlib = Extension("_nmtlib",
                    ["pymaster/namaster_wrap.c"],
                    libraries=libs,
                    include_dirs=[numpy_include, "../src/"],
                    extra_compile_args=extra,
                    )

setup(name="pymaster",
      description="Library for pseudo-Cl computation",
      author="David Alonso",
      version="0.9",
      packages=['pymaster'],
      ext_modules=[_nmtlib],
      )
