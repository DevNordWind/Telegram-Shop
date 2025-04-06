from aiogram_dialog import Dialog
from .window import cryptobot, cryptobot_info


payment_dialog = Dialog(
    cryptobot,
    cryptobot_info,
)