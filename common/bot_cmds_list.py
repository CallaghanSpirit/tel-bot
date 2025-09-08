from aiogram.types import BotCommand

private_commands = [
    BotCommand(command="/start", description="Запуск бота"),
    BotCommand(command="/menu", description="Меню"),
    BotCommand(command="/about", description="О боте"),
]