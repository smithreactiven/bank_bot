from aiogram import types, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from bot import keyboards, config
import tools


async def start_handler(message: types.Message):
    web_app_info = types.WebAppInfo(url=config.APP_URL)
    menu_btn = types.MenuButtonWebApp(
        text="Открыть",
        web_app=web_app_info
    )
    await message.bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=menu_btn
    )

    keyboard = InlineKeyboardBuilder()
    btn = InlineKeyboardButton(
        text="Открыть",
        web_app=web_app_info
    )
    keyboard.row(btn)
    msg_text = await tools.filer.read_txt('start')
    name = message.from_user.first_name
    await message.answer(
        text=msg_text.format(name),
        reply_markup=keyboard.as_markup()
    )


def setup(dp: Dispatcher):
    dp.message.register(start_handler, CommandStart())
