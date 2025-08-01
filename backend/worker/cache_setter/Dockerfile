FROM python:3.10-slim

WORKDIR /cache_setter

RUN pip install \
    pydantic==2.11.7 \
    pydantic-settings==2.10.1 \
    pika==1.3.2 \
    aio-pika==9.5.5 \
    redis==6.2.0

COPY ./core /core
COPY ./infrastructure/cache /infrastructure/cache
COPY ./infrastructure/messaging /infrastructure/messaging
COPY ./worker/cache_setter /cache_setter

CMD ["python", "main.py"]
