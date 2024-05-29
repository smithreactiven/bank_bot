from aiogram import types, Dispatcher
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters import CommandStart, Command, CommandObject
from sqlalchemy import select
from bot import keyboards, config, models
import tools


async def start_handler(message: types.Message, session, command: CommandObject):
    user_id = message.from_user.id

    if command.args:
        owner_user_id = re.findall(r"owner_referral_(\d+)", command.args)

        if not owner_user_id:
            return await message.answer(
                text="Такой реферальной ссылки нету, систему не обмануть("
            )
        else:
            owner_user_id = int(owner_user_id[0])

        if owner_user_id == user_id:
            return await message.answer(
                text="<b>Хорошая попытка,</b> но вы не можете активировать свою реферальную ссылку..."
            )

        async with session() as open_session:
            user = await open_session.execute(
                select(models.sql.User).filter_by(id=owner_user_id))
            user = user.scalars().first()

        if not user:
            return await message.answer(
                text="Такого пользователя <b>нет</b>. Проверьте вашу реферальную ссылку."
            )
        user = await open_session.execute(
            select(models.sql.User).filter_by(id=owner_user_id))
        user = user.scalars().first()

        referral = await open_session.execute(
            select(models.sql.OwnerReferral).filter_by(referral_user_id=user_id))
        referral = referral.scalars().first()

        if referral:
            return await message.answer(
                text="Вы уже являетесь рефералом какого-то пользователя."
            )
        else:
            new_referral = models.sql.OwnerReferral(
                referral_user_id=user_id,
                owner_user_id=owner_user_id
            )

            await open_session.merge(new_referral)
            await open_session.commit()

            msg_one = await tools.filer.read_txt('ok_referral')
            await message.answer(
                text=msg_one
            )
            msg_two = await tools.filer.read_txt('ok_referral_two')
            await message.bot.send_message(chat_id=owner_user_id, text=msg_two)
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
