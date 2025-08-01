FROM python:3.10-slim

WORKDIR /sample_data_generator

RUN pip install \
    pydantic==2.11.7 \
    pydantic-settings==2.10.1 \
    pika==1.3.2 \
    aio-pika==9.5.5

COPY ./core /core
COPY ./infrastructure/messaging /infrastructure/messaging
COPY ./worker/sample_data_generator /sample_data_generator

CMD ["python", "main.py"]
