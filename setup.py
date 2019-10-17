from setuptools import setup

setup(
    name='lucina',
    version='0.0.1',
    description='From markdown to Jupyter notebook',
    long_description='',
    url='https://pypi.org/project/lucina/',
    author='entwanne',
    author_email='antoine.rozo@gmail.com',
    packages=[],
    classifiers=['Development Status :: 1 - Planning'],
    entry_points = {
        'console_scripts': ['lucina=lucina.__main__'],
    }
)
