FROM python:3.8-slim

RUN apt update && \
    apt install --no-install-recommends -y gcc libc6-dev && \
    apt clean && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./topograph /app
WORKDIR /app
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
