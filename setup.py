from setuptools import find_packages
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


with open('lucina/_about.py') as f:
    about = {}
    exec(f.read(), about)


setup(
    name='lucina',
    version=about['__version__'],
    description='From markdown to Jupyter notebook',
    long_description=readme(),
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
            'isort',
        ]
    },
    license=about['__license__'],
    entry_points={
        'console_scripts': ['lucina=lucina.__main__:main'],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)
