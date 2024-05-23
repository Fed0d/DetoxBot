import app.keyboards as kb

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from model.detox import detox
import db.requests as rq

router = Router()


class ProcessText(StatesGroup):
    text = State()


@router.message(CommandStart())
async def process_start_command(message: types.Message):
    await rq.set_user(message.from_user.id)

    await message.reply('Привет!\n'
                        'Я - бот, который заменяет нецензурные слова на звёздочки.', reply_markup=kb.start)


@router.message(F.text == kb.button_texts['process_text'])
async def process_text(message: types.Message, state: FSMContext):
    await state.set_state(ProcessText.text)
    await message.answer('Отправьте мне текст, который нужно обработать.')


@router.message(ProcessText.text)
async def process_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer('Текст обрабатывается...')

    words = await rq.get_words()

    await message.answer(detox(data['text'], words))
    await state.clear()


@router.message(F.text == kb.button_texts['settings'])
async def process_settings(message: types.Message):
    await message.answer('Настройки пока не доступны.')


@router.message(F.text == kb.button_texts['help'])
async def process_help(message: types.Message):
    await message.answer('Помощь пока не доступна.')
