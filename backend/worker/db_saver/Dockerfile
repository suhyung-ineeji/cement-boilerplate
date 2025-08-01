FROM python:3.10-slim

WORKDIR /db_saver

RUN pip install \
    pydantic==2.11.7 \
    pydantic-settings==2.10.1 \
    pika==1.3.2 \
    aio-pika==9.5.5 \
    sqlalchemy==2.0.42 \
    asyncpg==0.30.0 \
    greenlet==3.2.3 \
    apscheduler==3.11.0

COPY ./core /core
COPY ./infrastructure/db /infrastructure/db
COPY ./infrastructure/messaging /infrastructure/messaging
COPY ./worker/db_saver /db_saver

CMD ["python", "main.py"]
