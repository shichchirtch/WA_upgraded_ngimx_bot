from aiogram import Router, html
import asyncio
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from lexicon import *
from python_db import users_db
from postgress_functions import (check_user_in_table, insert_new_user_in_table,
                            get_user_count,  return_orders)
from bot_instance import FSM_ST, dp, bot_storage_key, server_cart
from keyboards import show_my_orders_kb
from filters import SHOW_BUTTON


ch_router = Router()

@ch_router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    if not await check_user_in_table(user_id):
        print(message.from_user.id)

        await state.set_state(FSM_ST.after_start)
        await insert_new_user_in_table(user_id, user_name)
        bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
        bot_dict[message.from_user.id] = {'name':user_name, 'order':{}}  # Создаю пустой словарь для заметок юзера

        await dp.storage.update_data(key=bot_storage_key, data=bot_dict)  # Обновляю словарь бота

        insgesamt = await get_user_count() # Получаю общее количество уже запустивших бота

        server_cart[user_id] = []  # Создаю "учётную запись" для заказов юзера
        await message.answer(text=f'{html.bold(html.quote(user_name))}, '
                                  f'Hallo !\nI am MINI APP Bot'
                                  f'I have been already started <b>{insgesamt}</b> by users, like you 🎲',
                             parse_mode=ParseMode.HTML)
        await message.answer("Put on the Pizza Button please to open Web App ↙️",
                             reply_markup=show_my_orders_kb)
    else:
        print('start else works')
        await insert_new_user_in_table(user_id, user_name)
        server_cart[user_id] = []
        att = await message.answer(text='Bot was restated on server')
        await message.delete()
        await asyncio.sleep(2.5)
        await att.delete()


@ch_router.message(Command('help'))
async def help_command(message: Message):
    user_id = message.from_user.id
    temp_data = users_db[user_id]['bot_answer']
    if temp_data:
        await temp_data.delete()
    att = await message.answer(help_answer)
    users_db[user_id]['bot_answer'] = att
    await asyncio.sleep(2)
    await message.delete()


@ch_router.message(SHOW_BUTTON())
async def show_my_orders_command(message: Message):
    user_id = message.from_user.id

    ans_msg = await return_orders(user_id)

    await message.answer(ans_msg)

    await asyncio.sleep(2)
    await message.delete()


@ch_router.message(Command('about_project'))
async def about_project_command(message: Message):
    await message.answer(about_project)
    await asyncio.sleep(2)
    await message.delete()

@ch_router.message()
async def trasher(message: Message):
    print('TRASHER')
    await asyncio.sleep(1)
    await message.delete()