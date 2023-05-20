from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.methods.send_message import SendMessage
from pymongo.errors import DuplicateKeyError
from aiogram.fsm.context import FSMContext

from config import mongo, check_user
from .states import AdminInputStates

router = Router()

@router.callback_query(lambda c: c.data.startswith("publish_"))
async def publish(callback: CallbackQuery):
    text = callback.message.text + "\n\n✅ Одобрено к публикации"
    await callback.message.edit_text(text=text, reply_markup=None)
    command, user_id = callback.data.split("_")
    await SendMessage(
        chat_id=user_id,
        text="🎉 Ваше предложение к публикации одобрено! Пост появится на канале в течении 24 часов"
    )
    await callback.answer("✅ Успешно")


@router.callback_query(lambda c: c.data.startswith("ban_"))
async def ban(callback: CallbackQuery):
    command, user_id = callback.data.split("_")
    try:
        await mongo.banned.insert_one({
            '_id': int(user_id)
        })
    except DuplicateKeyError:
        return await callback.answer("❌ Данный пользователь уже заблокирован")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("✅ Пользователь заблокирован")


@router.callback_query(lambda c: c.data.startswith("answer_"))
async def answer(callback: CallbackQuery, state: FSMContext):
    command, user_id = callback.data.split("_")
    await state.set_data({'user': int(user_id)})
    await state.set_state(AdminInputStates.answer)
    await callback.answer("🤔 Введите ответ на вопрос")


@router.message(AdminInputStates.answer)
async def send_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    if await check_user(data['user']):
        return await message.answer("❌ Пользователь заблокирован")
    try:
        await SendMessage(
            chat_id=data['user'],
            text="Поступил ответ от администрации канала по Вашему вопросу:\n\n" + message.text
        )
        await message.answer("✅ Отправлено")
    except:
        await message.answer("❌ Не удалось отправить сообщение")
