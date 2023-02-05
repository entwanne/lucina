Lucina
======

From markdown to Jupyter notebook.

https://pypi.org/project/lucina/

Create a Jupyter notebook with Python & Markdown fragments from mardkwon files.

## Installation

Install Lucina by running `pip install lucina`.

## Usage

Running `lucina` on file [input.md](https://github.com/entwanne/lucina/tree/master/docs/input.md).

```shell
lucina -o docs/output.ipynb docs/input.md
```

It outputs file [output.ipynb](docs/output.ipynb) that looks like:

![Screenshot](https://github.com/entwanne/lucina/tree/master/docs/screen.png)

## Development

### Environment

Use `pip install -e '.[dev]'` to install `lucina` with development dependencies (tests & lint).

### Contributing

Code of the project is managed on <https://github.com/entwanne/lucina/> git repository.

### Building & deploying a new version

You need to install `twine` package (`pip install twine`) to be able to deploy a version of the library.

You can use `python setup.py sdist` to build the current version of the package.

Then you can deploy this version to PyPI by running `twine upload dist/*`.
