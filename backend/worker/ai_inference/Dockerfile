FROM python:3.10-slim

WORKDIR /ai_inference

RUN pip install \
    pydantic==2.11.7 \
    pydantic-settings==2.10.1 \
    pika==1.3.2 \
    aio-pika==9.5.5 \
    redis==5.0.0

COPY ./core /core
COPY ./infrastructure/messaging /infrastructure/messaging
COPY ./infrastructure/cache /infrastructure/cache
COPY ./worker/ai_inference /ai_inference

CMD ["python", "main.py"]
