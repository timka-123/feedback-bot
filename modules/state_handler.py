from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .states import UserInputState
from config import check_user

router = Router()

@router.message(UserInputState.question)
async def send_question(message: Message, state: FSMContext):
    if await check_user(message.from_user.id):
        return
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👍 Ответить", callback_data=f"answer_{message.from_user.id}"),
        InlineKeyboardButton(text="💥 Заблокировать", callback_data=f"ban_{message.from_user.id}")
    )
    await SendMessage(
        chat_id=1605007235,
        text=message.text,
        reply_markup=builder.as_markup()
    )
    await message.answer("✅ Отправлено")

@router.message(UserInputState.suggest)
async def send_question(message: Message, state: FSMContext):
    if await check_user(message.from_user.id):
        return
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👍 Опубликовать", callback_data=f"publish_{message.from_user.id}"),
        InlineKeyboardButton(text="💥 Заблокировать", callback_data=f"ban_{message.from_user.id}")
    )
    await SendMessage(
        chat_id=1605007235,
        text=message.text,
        reply_markup=builder.as_markup()
    )
    await message.answer("✅ Отправлено")
    