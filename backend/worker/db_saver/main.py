import sys
sys.path.append("..")

import asyncio
from asyncio import Queue
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.type.message import MessageType
from infrastructure.messaging.consumer.async_consumer import AsyncConsumer
from infrastructure.messaging.enum import RabbitMQQueue
from infrastructure.messaging.message import Message
from infrastructure.db.database import get_session_context

from infrastructure.db.orm.factory_data import FactoryDataEntity
from infrastructure.db.orm.predict_data import PredictDataEntity


messages = []
messages_lock = asyncio.Lock() # TODO: 락을 사용하지 않도록 수정 필요
consumer = AsyncConsumer()

async def enqueue_message(byte_msg: bytes):
    try:
        msg = Message.from_bytes(byte_msg)
        async with messages_lock:
            messages.append(msg)
    except Exception as e:
        print(f"[WARN] 메시지 파싱 실패: {e}")


async def batch_save_to_db():
    async with messages_lock:
        batch = messages.copy()
        messages.clear()

    if not batch:
        return

    async with get_session_context() as session:
        for msg in batch:
            match msg.message_type:
                case MessageType.FACTORY_DATA:
                    session.add(FactoryDataEntity(**msg.data))
                case MessageType.PREDICT_DATA:
                    session.add(PredictDataEntity(**msg.data))
                case _:
                    print(f"[WARN] 알 수 없는 메시지 타입: {msg.message_type}")
        await session.commit()
        print(f"[INFO] {len(batch)}건 저장 완료")



async def task():
    # 메시지 소비 백그라운드 실행
    asyncio.create_task(consumer.consume(queue_name=RabbitMQQueue.DB_SAVER, callback=enqueue_message))

    # 10초마다 배치 저장
    while True:
        await asyncio.sleep(10)
        await batch_save_to_db()


if __name__ == "__main__":
    asyncio.run(task())