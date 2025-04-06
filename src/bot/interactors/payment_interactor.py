import logging
from contextlib import suppress

from aiogram import Bot
from fluentogram import TranslatorHub
from sqlalchemy.orm import selectinload, joinedload

from src.db import Database
from src.db.enums import RefillStatus, Role
from src.db.models import Refill, User, Wallet


class PaymentInteractor:
    def __init__(self, bot: Bot, db: Database, translator: TranslatorHub):
        self.db = db
        self.bot = bot
        self.translator = translator

    async def on_payment_notification(self, refill_id: str):
        refill_status: RefillStatus | None = await self.db.refill.get_status(refill_id)
        if refill_status == RefillStatus.PENDING:
            await self.give_award(refill_id)

    async def give_award(self, refill_id: str):
        refill = await self.db.refill.get_by_where(
            whereclause=Refill.id == refill_id,
            options=(
                selectinload(Refill.wallet.and_(Wallet.currency == Refill.currency)),
                selectinload(Refill.user)
            )
        )
        refill.status = RefillStatus.SUCCESS
        refill.wallet.balance += refill.amount

        with suppress(Exception):
            user_translator = self.translator.get_translator_by_locale(refill.user.lang)
            await self.bot.send_message(
                chat_id=refill.user.user_id,
                text=user_translator.get(
                    'user-notify-payment',
                    amount=refill.amount,
                    currency=refill.currency,
                    payment_id=str(refill.id),
                )
            )

        await self.admin_mailing(
            'admin-notify-payment',
            is_username=str(bool(refill.user.username)),
            username=refill.user.username,
            first_name=refill.user.first_name,
            user_id=str(refill.user.user_id),
            amount=refill.amount,
            payment_method=refill.payment_method,
            currency=refill.currency,
            payment_id=str(refill.id)
        )
        await self.db.session.commit()

    async def cancel_payment(self, refill_id: str):
        refill = await self.db.refill.get_by_where(
            whereclause=Refill.id == refill_id,
            options=joinedload(Refill.user)
        )
        refill.status = RefillStatus.CANCELLED
        with suppress(Exception):
            translator = self.translator.get_translator_by_locale(refill.user.lang)
            await self.bot.send_message(
                chat_id=refill.user.user_id,
                text=translator.get(
                    'enter-code.notify-user-cancel',
                    id=refill.id
                )
            )
        await self.db.session.commit()

    async def admin_mailing(self, key: str, **kwargs):
        admins = await self.db.user.get_many(
            whereclause=((User.role == Role.ADMINISTRATOR) & (User.is_active == True)),
            limit=100
        )
        for admin in admins:
            translator = self.translator.get_translator_by_locale(admin.lang)
            with suppress(Exception):
                await self.bot.send_message(
                    chat_id=admin.user_id,
                    text=translator.get(key, **kwargs)
                )
