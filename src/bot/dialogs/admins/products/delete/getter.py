from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner

from src.cache.models import RedisUser
from src.db import Database
from src.db.models import Item


def get_data(dialog_manager: DialogManager) -> str:
    if dialog_manager.dialog_data:
        return dialog_manager.dialog_data['category_id']
    return dialog_manager.start_data['category_id']


@inject
async def approve_delete_categories_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    data_dict = {
        'categories_count': await db.category.count(),
        'positions_count': await db.position.count(),
        'items_count': await db.item.count(Item.purchase_id_fk == None)
    }
    dialog_manager.dialog_data.update(data_dict)
    return data_dict


@inject
async def approve_delete_positions_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    data_dict = {
        'positions_count': await db.position.count(),
        'items_count': await db.item.count(Item.purchase_id_fk == None)
    }
    dialog_manager.dialog_data.update(data_dict)
    return data_dict


@inject
async def approve_delete_items_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    data_dict = {
        'items_count': await db.item.count(Item.purchase_id_fk == None)
    }
    dialog_manager.dialog_data.update(data_dict)
    return data_dict


@inject
async def add_position_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    categories = await db.category.get_many_localized(redis_user.lang)
    btns = [
        (category.id, category.category_localized[0].name) for category in categories
    ]
    return {
        'btns': btns,
        'is_category_exist': bool(categories)
    }


@inject
async def browse_position_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs) -> dict:
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    bot: Bot = dialog_manager.middleware_data['bot']
    position_id = int(dialog_manager.dialog_data['position_id'])
    position = await db.position.get_localized_category(position_id, redis_user.lang, redis_user.currency)
    copy_link = await create_start_link(bot, f'start:position:{position_id}', encode=True)
    return {
        'category_name': position.category.category_localized[0].name,
        'position_name': position.position_localized[0].name,
        'price': position.position_price[0].price,
        'is_photo': bool(position.photoId) or bool(position.photo_file_name),
        'created_at': position.created_at,
        'is_description': bool(position.position_localized[0].description),
        'description': position.position_localized[0].description,
        'item_count': len(position.item),
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
async def browse_position_list_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs) -> dict:
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']
    positions = await db.position.get_many_localized_category(
        dialog_manager.dialog_data['category_id_fk'],
        redis_user.lang,
        redis_user.currency
    )

    return {
        'btns': [
            (
                position.id,
                translator.get(
                    'browse-position-list.position-btn',
                    name=position.position_localized[0].name,
                    price=position.position_price[0].price,
                    currency=redis_user.currency,
                    item_count=len(position.item)
                )
            )
            for position in positions
        ],
        'is_position': str(bool(positions))
    }
