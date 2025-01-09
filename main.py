import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from dotenv import load_dotenv

import quickstart

load_dotenv()


# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("You should set TOKEN environment variable")
    sys.exit(1)

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hola, {html.bold(message.from_user.full_name)}! \n Bienvenido al bot de cuentas de mercaditonic.com")

@dp.message(Command('deblist'))
async def list_users(message: Message):
    messages_to_send = quickstart.deb_list()
    if len(messages_to_send) == 0:
        await message.answer("No hay usuarios con pagos pendientes")

    else:
        # send message for each message in the list
        for message_to_send in messages_to_send:
            await message.answer(message_to_send)

@dp.message(Command('total_collected'))
async def total_collected(message: Message):
    total_collected_value = quickstart.total_collected_month()
    if total_collected_value == 0:
        await message.answer("No se ha recaudado dinero este mes")
    await message.answer(f"Total collected this month: {total_collected_value}")

@dp.message(Command('total_debt'))
async def total_debt(message: Message):
    total_debt_value = quickstart.total_debt_month()
    if total_debt_value == 0:
        await message.answer("No hay deudas pendientes este mes")
    await message.answer(f"Total debt this month: {total_debt_value}")

@dp.message(Command('clients_this_week'))
async def clients_this_week(message: Message):
    clients_this_week_list = quickstart.list_clients_this_week()
    if len(clients_this_week_list) == 0:
        await message.answer("No hay clientes con pagos pendientes esta semana")
    await message.answer(f"Clientes con pagos pendientes esta semana: {clients_this_week_list}")

@dp.message(Command('weekly_report'))
async def weekly_report(message: Message):
    quickly_report_values = quickstart.weekly_report()
    if quickly_report_values == None or len(quickly_report_values) == 0:
        await message.answer("No hay reporte semanal")
    else:
        # send message for each message in the list
        message_to_send = f"Cantidad de dinero recaudado esta semana: {quickly_report_values['total_collected']}\nCantidad de dinero adeudado esta semana: {quickly_report_values['total_debt']}\nClientes con pagos pendientes esta semana: {quickly_report_values['clients_this_week']}"
        await message.answer(message_to_send)

@dp.message(Command('monthly_report'))
async def monthly_report(message: Message):
    quickly_report_values = quickstart.monthly_report()
    if quickly_report_values == None or len(quickly_report_values) == 0:
        await message.answer("No hay reporte mensual")
    else:
        # send message for each message in the list
        message_to_send = f"Cantidad de dinero recaudado este mes: {quickly_report_values['total_collected']}\nCantidad de dinero adeudado este mes: {quickly_report_values['total_debt']}\nClientes con pagos pendientes este mes: {quickly_report_values['clients_this_week']}"
        await message.answer(message_to_send)


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Comandos disponibles: \n /deblist - Lista de usuarios con pagos pendientes \n /total_collected - Total recaudado este mes \n /total_debt - Total adeudado este mes \n /clients_this_week - Clientes con pagos pendientes esta semana \n /weekly_report - Reporte semanal \n /monthly_report - Reporte mensual")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
