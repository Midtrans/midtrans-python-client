> Warning: This note is for developer/maintainer of this package only

## Updating Package

- Make your changes
- Update version on `./setup.py` file
- To run test, run `pytest`
- To install the package locally with a symlink `pip install -e .`
- To update https://pypi.org repo, run these on terminal:
```bash
# install setuptools & wheel
python -m pip install --upgrade setuptools wheel

# Generate `dist/` folder for upload
python setup.py sdist bdist_wheel

# Update / install Twine
python -m pip install --upgrade twine;

# upload to pypi / pip repository
# you will be asked for username and password for https://pypi.org account
twine upload dist/*;

# To upload to test pypi use this instead
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*;
```