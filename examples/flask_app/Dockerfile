from python:3.7-alpine
LABEL name "midflask"

# Create app directory
WORKDIR /usr/src/midtrans-payment-example-app

COPY . .

RUN pip install pipenv

RUN pipenv install --system --deploy
EXPOSE 5000
CMD ["python", "web.py"]