from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from sqlalchemy.orm import selectinload

from src.bot.utilities import get_pages
from src.cache.models import RedisUser
from src.db import Database
from src.db.models import Category, CategoryLocalized


@inject
async def select_category_add_item_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']

    height = 10

    widget: ManagedScroll = dialog_manager.find("CATEGORY_SCROLL")
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


@inject
async def select_position_add_item_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    category_id_fk = dialog_manager.dialog_data.get('category_id_fk')

    positions = await db.position.get_many_localized_category(
        category_id_fk, redis_user.lang, redis_user.currency
    )

    return {
        'btns': [
            (
                position.id,
                translator.get(
                    'select-position-add-items.position-btn',
                    name=position.position_localized[0].name,
                    price=position.position_price[0].price,
                    item_count=len(position.item),
                    currency=redis_user.currency
                )
            )
            for position in positions
        ],
        'is_position': str(bool(positions))
    }
