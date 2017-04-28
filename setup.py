import os

from setuptools import setup
from rawkit import VERSION


def readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
        return f.read()


setup(
    name='rawkit',
    version=VERSION,
    description='CTypes based LibRaw bindings',
    author='Cameron Paul, Sam Whited',
    author_email='cpaul37@gmail.com',
    maintainer='Cameron Paul, Sam Whited',
    maintainer_email='sam@samwhited.com',
    url='https://rawkit.readthedocs.org',
    packages=['rawkit', 'libraw'],
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
    extras_require={'doc': ['sphinx >= 1.3']},
)
