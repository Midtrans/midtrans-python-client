> Warning: This note is for developer/maintainer of this package only

## Updating Package

- If from scratch, using `pipenv`
	- Install pipenv `pip install pipenv` or `pip3 install pipenv`
		- If fail, you may need to prefix the command with `sudo `
	- CD to project directory
	- Install using pipenv `pipenv install`
		- If fail, you may need to specify which python bin file by `pipenv install --python /usr/bin/python3`. (Run `which python` or `which python3` to know the file path)
	- Activate and enter python env for current folder `pipenv shell`, now you are inside python env
	- Install project as local package `pip install -e .`
- Make your code changes
- Increase `version` value on:
    - `./setup.py` file
    - `./midtransclient/__init__.py` file
    - `./midtransclient/http_client.py` file on User-Agent value
- To install the package locally with a symlink `pip install -e .`
- To run test, run `pytest`
	- To run specific test, e.g: `pytest -k "test_core_api_charge_fail_401"`
	- If fail, you may need to install pytest first `pip install pytest`
- To update https://pypi.org repo, run these on terminal:
```bash
# install setuptools & wheel
python -m pip install --upgrade setuptools wheel

# Generate `dist/` folder for upload
python setup.py sdist bdist_wheel

# Update / install Twine
python -m pip install --upgrade twine

# upload to pypi / pip repository
# you will be asked for username and password for https://pypi.org account
twine upload dist/* --skip-existing

# To upload to test pypi use this instead
# twine upload --repository-url https://test.pypi.org/legacy/ dist/* --skip-existing;
```
	- if fail to upload, clean up all files within your `./dist` folder, then re-try the above commands

## Dev & Test via Docker Compose

- To use docker-compose to test and run project, `cd` to repo dir
- Run `docker-compose up`, which basically run pytest on container
- Run `docker-compose down`, to clean up when done