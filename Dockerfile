# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

# Start app
# CMD ["gunicorn", "main2:app"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3100"] # Maybe this works for custom containers
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]
# Connection String
ENV APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=ec500fd4-d1b0-48e4-8bea-85d15385b671;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/;ApplicationId=4592960f-3e47-45b7-bae3-7c9e9d788943

# Attach
# ENV PYTHONPATH="/code/sitecustomize"

# # For ssh
# COPY entrypoint.sh ./
# # Start and enable SSH
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends dialog \
#     && apt-get install -y --no-install-recommends openssh-server \
#     && echo "root:Docker!" | chpasswd \
#     && chmod u+x ./entrypoint.sh
# COPY sshd_config /etc/ssh/
# EXPOSE 8000 2222
# ENTRYPOINT [ "./entrypoint.sh" ] 