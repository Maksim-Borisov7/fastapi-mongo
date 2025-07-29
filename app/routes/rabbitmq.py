from faststream.rabbit.fastapi import RabbitRouter

router = RabbitRouter()


async def send_notification():
    await router.broker.publish(
        f"Ваш заказ успешно оплачен",
        queue="orders",
    )
    return {'data': "OK"}