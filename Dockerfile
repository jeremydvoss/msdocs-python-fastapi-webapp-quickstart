# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

ENV APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=ec500fd4-d1b0-48e4-8bea-85d15385b671;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/

ENV PYTHONPATH="/code/sitecustomize"

CMD ["gunicorn", "main:app"]