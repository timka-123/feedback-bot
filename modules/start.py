from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from .states import UserInputState
from config import check_user

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    if await check_user(message.from_user.id):
        return
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🤔 Задать вопрос", callback_data="question"),
        InlineKeyboardButton(text="👍 Предложить пост", callback_data="suggest")
    )
    await message.answer("Привет 👋\nИспользуй кнопки ниже, чтобы задать вопрос, либо предложить пост",
                         reply_markup=builder.as_markup())


@router.callback_query(Text("question"))
async def question(callback: CallbackQuery, state: FSMContext):
    if await check_user(callback.from_user.id):
        return
    await state.set_state(UserInputState.question)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    )
    await callback.message.edit_text(text="❓ Введите свой вопрос, и администрация на него ответит! Пожалуйста, загружайте картинки на файлообменники, бот временно не пересылает их.",
                                     reply_markup=builder.as_markup())


@router.callback_query(Text("suggest"))
async def suggest(callback: CallbackQuery, state: FSMContext):
    if await check_user(callback.from_user.id):
        return
    await state.set_state(UserInputState.suggest)
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    )
    await callback.message.edit_text(text="💡 Введи пост так, как будто ты пишешь его в канал! Пожалуйста, загружайте картинки на файлообменники, бот временно не пересылает их.",
                                     reply_markup=builder.as_markup())


@router.callback_query(Text("cancel"))
async def cancel(callback: CallbackQuery, state: FSMContext):
    if await check_user(callback.from_user.id):
        return
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🤔 Задать вопрос", callback_data="question"),
        InlineKeyboardButton(text="👍 Предложить пост", callback_data="suggest")
    )
    await callback.message.edit_text(text="Привет 👋\nИспользуй кнопки ниже, чтобы задать вопрос, либо предложить пост",
                         reply_markup=builder.as_markup())
