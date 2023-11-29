# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 3100

# Start app
# CMD ["gunicorn", "main:app"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3100"]

# Connection String
ENV APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=ec500fd4-d1b0-48e4-8bea-85d15385b671;IngestionEndpoint=https://centralus-2.in.applicationinsights.azure.com/;LiveEndpoint=https://centralus.livediagnostics.monitor.azure.com/

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