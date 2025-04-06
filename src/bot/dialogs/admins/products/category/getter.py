from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from sqlalchemy.orm import selectinload

from src.bot.utilities import get_pages
from src.cache.models import RedisUser
from src.db import Database
from src.db.enums import Lang
from src.db.models import Category, CategoryLocalized


def get_data(dialog_manager: DialogManager) -> str:
    if dialog_manager.dialog_data:
        return dialog_manager.dialog_data['category_id']
    return dialog_manager.start_data['category_id']


async def input_category_name_ru_getter(dialog_manager: DialogManager, **kwargs):
    edit_mode = dialog_manager.dialog_data.get('edit_mode')
    return {
        'edit_mode': True if edit_mode is not None or edit_mode == True else False
    }


def get_lang(dialog_manager: DialogManager, redis_user: RedisUser) -> Lang:
    temp_lang: str | None = dialog_manager.dialog_data.get('temp_lang')
    if temp_lang:
        return Lang(temp_lang)
    return redis_user.lang




@inject
async def edit_category_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    category_id = int(get_data(dialog_manager))
    bot: Bot = dialog_manager.middleware_data['bot']
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    category, position_count, item_amount = (await db.category.get_browse_category(
        category_id, get_lang(dialog_manager, redis_user)
    ))[0]

    copy_link = await create_start_link(bot, f'start:category:{category_id}', encode=True)
    return {
        'category_name': category.category_localized[0].name,
        'position_count': position_count,
        'item_amount': item_amount,
        'created_at': category.created_at,
        'purchase_day_count': 0,
        'purchase_week_count': 0,
        'purchase_month_count': 0,
        'purchase_day_amount': 0,
        'purchase_week_amount': 0,
        'purchase_month_amount': 0,
        'purchase_all_amount': 0,
        'purchase_all_count': 0,
        'copy_link': copy_link,
        'currency': redis_user.currency
    }


@inject
async def category_list_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']

    height = 10

    widget: ManagedScroll = dialog_manager.find("CATEGORIES_SCROLL")
    page = await widget.get_page()

    offset = page * height
    limit = height

    categories = await db.category.get_pagination(
        options=selectinload(Category.category_localized.and_(CategoryLocalized.lang == redis_user.lang)),
        offset=offset,
        limit=limit,
        order_by=Category.id,
    )

    categories_count: int = await db.category.count()

    return {
        'btns': [(category.id, category.category_localized[0].name) for category in categories],
        'is_category': str(bool(categories)),
        'pages': get_pages(height=height, items=categories_count)
    }
