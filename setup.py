import os

from setuptools import setup
from rawkit import VERSION


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        return f.read()

setup(
    name='rawkit',
    version=VERSION,
    description='CTypes based LibRaw bindings',
    author='Cameron Paul, Sam Whited',
    author_email='cpaul37@gmail.com',
    url='https://photoshell.github.io/rawkit/',
    packages=['rawkit'],
    keywords=['encoding', 'images', 'photography', 'libraw', 'raw', 'photos'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=readme(),
    tests_require=[
        'pytest >= 3.7.1',
        'tox >= 2.0.1',
        'mock >= 1.0.1'
    ],
    extras_require={'doc': ['Sphinx >=1.0']},
)
