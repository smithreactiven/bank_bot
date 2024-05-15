from aiogram import types, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from sqlalchemy import select
from bot import keyboards, config, models
import tools


async def start_handler(message: types.Message, session):
    async with session() as open_session:
        user_in_db = await open_session.execute(select(models.sql.User).filter_by(id=message.from_user.id))
        user_in_db = user_in_db.scalars().first()
        if not user_in_db:
            new_user = models.sql.User(
                id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                check=0
            )
            await open_session.merge(new_user)
            await open_session.commit()
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
