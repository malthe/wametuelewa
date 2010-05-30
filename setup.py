__version__ = '0.2'

import os
import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

version = sys.version_info[:3]

install_requires = [
    "Lepl",
    'Django',
    ]

setup(
    name="Wametuelewa",
    version=__version__,
    description="Messaging platform for Django.",
    long_description="\n\n".join((README, CHANGES)),
    classifiers=[
       "Development Status :: 3 - Alpha",
       "Intended Audience :: Developers",
       "Programming Language :: Python",
       "Operating System :: POSIX",
      ],
    keywords="sms parsing",
    author="Malthe Borch",
    author_email="mborch@gmail.com",
    install_requires=install_requires,
    license='BSD',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    tests_require = install_requires,
    )

