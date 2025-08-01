FROM python:3.10-slim

WORKDIR /application

RUN pip install \
    pydantic==2.11.7 \
    pydantic-settings==2.10.1 \
    pika==1.3.2 \
    aio-pika==9.5.5 \
    redis==5.0.0 \
    fastapi==0.116.1 \
    uvicorn==0.35.0

COPY ./core /core
COPY ./infrastructure/messaging /infrastructure/messaging
COPY ./infrastructure/cache /infrastructure/cache
COPY ./infrastructure/db /infrastructure/db
COPY ./application /application

CMD ["python", "main.py"]
