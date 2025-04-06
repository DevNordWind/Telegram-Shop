from dishka import AsyncContainer

from src.cache import Cache
from src.payments import PaymentCreator
from src.payments.enums import PaymentMethod


async def on_startup(async_container: AsyncContainer):
    cache: Cache = await async_container.get(Cache)
    async with async_container() as container:
        payment_creator = await container.get(PaymentCreator)
        pay_mg = await payment_creator.get(PaymentMethod.CRYPTOBOT)
        rub_usd = '0.011'
        if await pay_mg.is_available():
            rates = await pay_mg.cb.get_exchange_rates()
            for rate in rates:
                if rate.source == "RUB" and rate.target == "USD":
                    rub_usd = str(rate.rate)

    if not await cache.bot_settings.get_by_key('settings'):
        await cache.bot_settings.new(
            status_buy=False,
            status_refill=False,
            status_cryptobot=False,
            status_work=False,
            rub_usd=rub_usd
        )