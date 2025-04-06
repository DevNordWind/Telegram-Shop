from dataclasses import dataclass
from datetime import datetime, timedelta, time
from decimal import Decimal

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.bot.utilities import convert_currency
from src.cache.models import RedisUser, BotSettings
from src.db import Database
from src.db.enums import Currency, RefillCause, RefillStatus
from src.db.models import Item, Purchase, Refill
from src.payments.enums import PaymentMethod


@dataclass
class TimePoints:
    day: datetime
    week: datetime
    month: datetime


def get_time_points() -> TimePoints:
    today = datetime.today()
    day = datetime.combine(today, time.min)
    week = today - timedelta(days=today.weekday())
    month = datetime(today.year, today.month, 1, 0, 0, 0)
    return TimePoints(
        day=day,
        week=week,
        month=month
    )


async def user_statistic(db: Database, time_points: TimePoints) -> dict:
    all_users = await db.user.get_many(limit=None)
    users_day = 0
    users_week = 0
    users_month = 0
    users_all = len(all_users)

    for user in all_users:
        if user.reg_time >= time_points.day:
            users_day += 1
        if user.reg_time >= time_points.week:
            users_week += 1
        if user.reg_time >= time_points.month:
            users_month += 1
    return {
        'users_day': users_day,
        'users_week': users_week,
        'users_month': users_month,
        'users_all': users_all
    }


async def purchase_statistic(
        db: Database,
        time_points: TimePoints,
        current_currency: Currency,
        rub_usd_rate: Decimal
) -> dict:
    purchases = await db.purchase.get_many()
    profit_count_day, profit_amount_day = 0, 0
    profit_count_week, profit_amount_week = 0, 0
    profit_count_month, profit_amount_month = 0, 0
    profit_count_all, profit_amount_all = len(purchases), 0
    for purchase in purchases:
        if purchase.created_at >= time_points.day:
            profit_count_day += 1
            profit_amount_day += convert_currency(
                rub_usd_rate=rub_usd_rate,
                source=Currency(purchase.currency),
                target=current_currency,
                amount=purchase.amount
            )
        if purchase.created_at >= time_points.week:
            profit_count_week += 1
            profit_amount_week += convert_currency(
                rub_usd_rate=rub_usd_rate,
                source=Currency(purchase.currency),
                target=current_currency,
                amount=purchase.amount
            )
        if purchase.created_at >= time_points.month:
            profit_count_month += 1
            profit_amount_month += convert_currency(
                rub_usd_rate=rub_usd_rate,
                source=Currency(purchase.currency),
                target=current_currency,
                amount=purchase.amount
            )
        profit_amount_all += convert_currency(
            rub_usd_rate=rub_usd_rate,
            source=Currency(purchase.currency),
            target=current_currency,
            amount=purchase.amount
        )
    return {
        'profit_count_day': profit_count_day,
        'profit_amount_day': profit_amount_day,
        'profit_count_week': profit_count_week,
        'profit_amount_week': profit_amount_week,
        'profit_count_month': profit_count_month,
        'profit_amount_month': profit_amount_month,
        'profit_count_all': profit_count_all,
        'profit_amount_all': profit_amount_all
    }


async def refill_statistics(
        db: Database,
        time_points: TimePoints,
        current_currency: Currency,
        rub_usd_rate: Decimal
):
    refills = await db.refill.get_many(
        (Refill.status == RefillStatus.SUCCESS) & (Refill.cause == RefillCause.PAYMENT)
    )
    refill_count_day, refill_amount_day = 0, 0
    refill_count_week, refill_amount_week = 0, 0
    refill_count_month, refill_amount_month = 0, 0
    refill_count_all, refill_amount_all = len(refills), 0
    users_money_give = 0
    refill_cryptobot_count, refill_cryptobot_amount = 0, 0
    refill_steam_count, refill_steam_amount = 0, 0
    for refill in refills:
        if refill.status == RefillStatus.SUCCESS:
            if refill.created_at >= time_points.day:
                refill_count_day += 1
                refill_amount_day += convert_currency(
                    rub_usd_rate=rub_usd_rate,
                    source=Currency(refill.currency),
                    target=current_currency,
                    amount=refill.amount
                )
            if refill.created_at >= time_points.week:
                refill_count_week += 1
                refill_amount_week += convert_currency(
                    rub_usd_rate=rub_usd_rate,
                    source=Currency(refill.currency),
                    target=current_currency,
                    amount=refill.amount
                )
            if refill.created_at >= time_points.month:
                refill_count_month += 1
                refill_amount_month += convert_currency(
                    rub_usd_rate=rub_usd_rate,
                    source=Currency(refill.currency),
                    target=current_currency,
                    amount=refill.amount
                )
            refill_amount_all += convert_currency(
                rub_usd_rate=rub_usd_rate,
                source=Currency(refill.currency),
                target=current_currency,
                amount=refill.amount
            )
            if refill.cause == RefillCause.GIFT:
                users_money_give += convert_currency(
                    rub_usd_rate=rub_usd_rate,
                    source=Currency(refill.currency),
                    target=current_currency,
                    amount=refill.amount
                )
            if refill.payment_method == PaymentMethod.CRYPTOBOT:
                refill_cryptobot_count += 1
                refill_cryptobot_amount += convert_currency(
                    rub_usd_rate=rub_usd_rate,
                    source=Currency(refill.currency),
                    target=current_currency,
                    amount=refill.amount
                )
    return {
        'refill_count_day': refill_count_day,
        'refill_amount_day': refill_amount_day,
        'refill_count_week': refill_count_week,
        'refill_amount_week': refill_amount_week,
        'refill_count_month': refill_count_month,
        'refill_amount_month': refill_amount_month,
        'refill_count_all': refill_count_all,
        'refill_amount_all': refill_amount_all,
        'users_money_give': users_money_give,
        'refill_steam_amount': refill_steam_amount,
        'refill_steam_count': refill_steam_count,
        'refill_cryptobot_amount': refill_cryptobot_amount,
        'refill_cryptobot_count': refill_cryptobot_count,
    }


@inject
async def statistic_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    time_points: TimePoints = get_time_points()
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    users_statistic: dict = await user_statistic(db, time_points)
    purchases_statistic: dict = await purchase_statistic(db, time_points, redis_user.currency,
                                                         Decimal(bot_settings.rub_usd))
    refills_statistic: dict = await refill_statistics(db, time_points, redis_user.currency,
                                                      Decimal(bot_settings.rub_usd))

    items_count = await db.item.count(Item.purchase_id_fk == None)
    positions_count = await db.position.count()
    categories_count = await db.category.count()

    return {
        **users_statistic,
        **purchases_statistic,
        **refills_statistic,
        'items_count': items_count,
        'positions_count': positions_count,
        'categories_count': categories_count,
        'now_day': time_points.day,
        'week_day': time_points.week,
        'month_day': time_points.month
    }
