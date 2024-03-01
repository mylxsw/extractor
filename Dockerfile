# install packages
FROM python:3.11-slim-bookworm as packages

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev

COPY requirements.txt /requirements.txt
RUN pip install --prefix=/pkg -r requirements.txt

# production stage
FROM python:3.11-slim-bookworm AS production

EXPOSE 80
WORKDIR /app

COPY --from=packages /pkg /usr/local
COPY . /app

CMD ["gunicorn", "--worker-class", "gevent", "--workers", "2", "--bind", "0.0.0.0:80", "--access-logfile", "-", "app:app"]