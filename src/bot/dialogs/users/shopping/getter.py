from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from sqlalchemy.orm import selectinload

from src.bot.utilities import get_pages, MediaHelper
from src.bot.utilities.media_helper.exceptions import NeedUpdate
from src.cache.models import RedisUser, BotSettings
from src.db import Database
from src.db.models import Category, CategoryLocalized, Position, PositionLocalized, PositionPrice, Item


@inject
async def select_category_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data["redis_user"]
    bot_settings: BotSettings = dialog_manager.middleware_data["bot_settings"]

    page_size = 10
    widget: ManagedScroll = dialog_manager.find("CATEGORIES_SCROLL")
    page = await widget.get_page()

    offset = page * page_size

    categories = await db.category.get_shopping(
        lang=redis_user.lang,
        offset=offset,
        limit=page_size,
        category_without_items=bot_settings.category_without_items
    )

    categories_count = await db.category.get_count_shopping(bot_settings.category_without_items)
    return {
        'btns': [(category[0], category[1]) for category in categories],
        'pages': get_pages(height=page_size, items=categories_count),
        **bot_settings.__dict__
    }


@inject
async def select_position_getter(dialog_manager: DialogManager, db: FromDishka[Database], **kwargs):
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    bot_settings: BotSettings = dialog_manager.middleware_data['bot_settings']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']

    height = 10

    widget: ManagedScroll = dialog_manager.find("POSITION_SCROLL")
    page = await widget.get_page()
    offset = page * height
    limit = height

    category_id_fk: int = int(dialog_manager.dialog_data.get('category_id_fk'))

    positions = await db.position.get_shopping(
        category_id_fk,
        redis_user.lang,
        redis_user.currency,
        bot_settings.position_without_items,
        offset,
        limit
    )
    position_count: int = await db.position.get_count_shopping(
        category_id_fk=category_id_fk,
        position_without_items=bot_settings.position_without_items
    )
    currency_symbol = translator.get('currency_symbol_by_enum', currency=redis_user.currency)

    return {
        'btns': [(position[0], position[1], position[2], currency_symbol)
                 for position in positions],
        'pages': get_pages(height=height, items=position_count),
    }


@inject
async def position_details_getter(dialog_manager: DialogManager, db: FromDishka[Database],
                                  media_helper: FromDishka[MediaHelper], **kwargs):
    position_id: int = int(dialog_manager.dialog_data.get('position_id'))
    redis_user: RedisUser = dialog_manager.middleware_data['redis_user']
    translator: TranslatorRunner = dialog_manager.middleware_data['translator']

    position = await db.position.get_by_where(
        Position.id == position_id,
        options=(
            selectinload(Position.item.and_(Item.purchase_id_fk == None)),
            selectinload(Position.position_localized.and_(PositionLocalized.lang == redis_user.lang)),
            selectinload(Position.position_price.and_(PositionPrice.currency == redis_user.currency)),
            selectinload(Position.category).selectinload(
                Category.category_localized.and_(CategoryLocalized.lang == redis_user.lang))
        )
    )

    data_dict = {
        'position_name': position.position_localized[0].name,
        'category_name': position.category.category_localized[0].name,
        'price': str(position.position_price[0].price),
        'currency': redis_user.currency,
        'items_count': str(len(position.item)) if position.item else '0'
    }

    text = translator.get(
        'position-details',
        **data_dict
    )

    if position.position_localized[0].description is not None:
        text += '\n' + translator.get(
            'position-details.description',
            description=position.position_localized[0].description
        )

    media = None

    if position.file_id is not None and position.file_path is not None:
        try:
            media = await media_helper.get(position.content_type).get_media_attachment(
            chat_id=dialog_manager.event.from_user.id,
            file_id=position.file_id,
            file_path=position.file_path,
        )
        except NeedUpdate as e:
            print(e)
            media = e.media_attachment
            position.file_id = media.file_id.file_id
            await db.session.commit()
        except Exception as e:
            print(e)
            media = None
    return {
        'text': text,
        'media': media
    }


async def input_amount_item_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        **dialog_manager.dialog_data
    }


async def approve_buy_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        **dialog_manager.dialog_data
    }


async def receipt_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    return {
        **dialog_manager.dialog_data
    }
