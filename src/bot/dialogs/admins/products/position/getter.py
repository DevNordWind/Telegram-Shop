import math

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from sqlalchemy import and_
from sqlalchemy.orm import selectinload

from src.bot.utilities import get_pages
from src.bot.utilities.media_helper import MediaHelper
from src.bot.utilities.media_helper.exceptions import NeedUpdate
from src.cache.models import RedisUser
from src.db import Database
from src.db.enums import Lang
from src.db.models import Item, Category, CategoryLocalized


@inject
async def category_list_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']

    height = 10

    widget: ManagedScroll = dialog_manager.find("CATEGORIES_SCROLL_SELECT")
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


async def add_position_name_ru_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        'switch_from_category': bool(dialog_manager.dialog_data.get('switch_from_category')),
        'edit_mode': bool(dialog_manager.dialog_data.get('edit_mode'))
    }


def get_lang(dialog_manager: DialogManager, redis_user: RedisUser) -> Lang:
    temp_lang: str | None = dialog_manager.dialog_data.get('temp_lang')
    if temp_lang:
        return Lang(temp_lang)
    return redis_user.lang


async def add_position_price_rub_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'edit_mode': bool(dialog_manager.dialog_data.get('edit_mode'))
    }


async def add_position_photo_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'edit_mode': bool(dialog_manager.dialog_data.get('edit_mode'))
    }


async def add_position_description_ru_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'edit_mode': bool(dialog_manager.dialog_data.get('edit_mode'))
    }


def get_position_id(dialog_manger: DialogManager) -> int:
    if dialog_manger.dialog_data.get('position_id') is not None:
        return int(dialog_manger.dialog_data.get('position_id'))
    return int(dialog_manger.start_data.get('position_id'))


@inject
async def edit_position_getter(dialog_manager: DialogManager, db: FromDishka[Database],
                               media_fix: FromDishka[MediaHelper],
                               **kwargs) -> dict:
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    bot: Bot = dialog_manager.middleware_data['bot']
    position_id = get_position_id(dialog_manager)

    lang = get_lang(dialog_manager, redis_user)

    position = await db.position.get_localized_category(position_id, lang, redis_user.currency)
    copy_link = await create_start_link(bot, f'start:position:{position_id}', encode=True)
    is_media = bool(position.file_path or position.file_id)
    data_to_return = {
        'category_name': position.category.category_localized[0].name,
        'position_name': position.position_localized[0].name,
        'price': position.position_price[0].price,
        'created_at': position.created_at,
        'is_description': str(bool(position.position_localized[0].description)),
        'description': position.position_localized[0].description,
        'item_count': len(position.item),
        'is_media': str(is_media),
        'purchase_day_count': 0,
        'purchase_week_count': 0,
        'purchase_month_count': 0,
        'purchase_day_amount': 0,
        'purchase_week_amount': 0,
        'purchase_month_amount': 0,
        'purchase_all_amount': 0,
        'purchase_all_count': 0,
        'copy_link': copy_link,
        'currency': redis_user.currency,
        'category_id_fk': bool(dialog_manager.dialog_data.get('category_id_fk'))
    }

    if is_media:
        fixer = media_fix.get(position.content_type)
        try:
            media = await fixer.get_media_attachment(
                chat_id=dialog_manager.event.from_user.id,
                file_id=position.file_id,
                file_path=position.file_path,
                caption=dialog_manager.middleware_data['translator'].get('upload',
                                                                         content_type=fixer.content_type.value)
            )
            data_to_return.update(
                {
                    'media': media
                }
            )
        except NeedUpdate as e:
            position.file_id = e.media_id
            data_to_return.update(
                {
                    'media': e.media_attachment
                }
            )
            await db.session.commit()
    return data_to_return


@inject
async def positions_list_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs) -> dict:
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
                    'positions-list.position-btn',
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


def prepare_item_text(text: str) -> str:
    if '\n' not in text:
        return text[:64]
    split_text = text.split('\n')
    return ' '.join(split_text)[:64]


@inject
async def items_list_getter(
        dialog_manager: DialogManager,
        db: FromDishka[Database],
        **kwargs
):
    position_id_fk = int(dialog_manager.dialog_data.get('position_id'))

    height = 8

    widget: ManagedScroll = dialog_manager.find("ITEMS_SCROLL")
    page = await widget.get_page()

    offset = page * height
    limit = height

    whereclause = and_(
            Item.purchase_id_fk == None,
            Item.position_id_fk == position_id_fk
        )

    items = await db.item.get_pagination(
        offset=offset,
        limit=limit,
        order_by=Item.id,
        wheraclause=whereclause
    )
    items_count = await db.item.count(whereclause=whereclause)

    return {
        'btns': [(item.id, prepare_item_text(item.content)) for item in items],
        'pages': get_pages(height=height, items=items_count),
    }
@inject
async def item_details_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    item = await db.item.get_with_category_position(
        item_id=dialog_manager.dialog_data['item_id'],
        lang=dialog_manager.middleware_data['redis_user'].lang
    )

    return {
        'category_name': item.category.category_localized[0].name,
        'position_name': item.position.position_localized[0].name,
        'created_at': item.created_at,
        'content': item.content
    }