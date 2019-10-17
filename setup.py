
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
ext_modules = [
    # Extension("oauth2client",  ["oauth2client.py"]),
    # Extension("mymodule2",  ["mymodule2.py"]),
#   ... all your modules that need be compiled ...
]
setup(
    name = 'Mail Send',
   #  cmdclass = {'build_ext': build_ext},
    ext_modules = cythonize('send.pyx')
)
