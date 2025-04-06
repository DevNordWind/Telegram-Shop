from aiogram_dialog import Window

from src.bot.dialogs.admins.statistic.getter import statistic_getter
from src.bot.states import StatisticState
from src.bot.widgets import GetText

statistic = Window(
    GetText('statistic'),

    getter=statistic_getter,
    state=StatisticState.statistic
)