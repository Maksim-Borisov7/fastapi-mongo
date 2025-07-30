from faststream.rabbit.fastapi import RabbitRouter

from app.config import settings

router = RabbitRouter()


async def send_notification():
    await router.broker.publish(
        f"Ваш заказ успешно оплачен",
        queue=settings.QUEUE_ORDERS
    )
    return {'data': "OK"}
