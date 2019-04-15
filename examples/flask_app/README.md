# Sample Flask App

Example of checkout page using Midtrans Snap. A quick and secure way to accept
payment with a beautiful user interface done for you.

This is a very simple, very minimalist example to demonstrate integrating
Midtrans Snap with Flask (Python). To start:

## Run Natively / Without Docker

1. Install Python (3.6.0, for instance, as used by this example)
2. Clone the repository
3. Install flask: `pip install Flask`
4. Install midtrans: `pip install midtransclient`
5. Run the web server using:
	- `python web.py`, or
	- `FLASK_APP=web.py flask run`,

> Or replace step 3 & 4 by `pipenv install`, if you are using pipenv.

The app will run at port 5000.

## Run With Docker
> required: Docker installed.

- First time to build & run: `docker build -t midflask . && docker run -p 5000:5000 --rm -it midflask`.
- Next time just run `docker run -p 5000:5000 --rm -it midflask`
