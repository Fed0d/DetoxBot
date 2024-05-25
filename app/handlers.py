import app.keyboards as kb
import io

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, BufferedInputFile

from model.detox import detox
import db.requests as rq

router = Router()


class ProcessText(StatesGroup):
    text = State()


class AddWords(StatesGroup):
    words = State()


class RemoveWords(StatesGroup):
    words = State()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply('Привет!\n'
                        'Я - бот, который заменяет нецензурные слова на звёздочки.', reply_markup=kb.start)


@router.message(Command('process_text'))
@router.message(F.text == kb.button_texts['process_text'])
async def process_text(message: Message, state: FSMContext):
    await state.set_state(ProcessText.text)
    await message.answer('Отправьте мне текст, который нужно обработать.', reply_markup=kb.back_to_start)


@router.message(Command('settings'))
@router.message(F.text == kb.button_texts['settings'])
async def process_settings(message: Message):
    await message.answer('Выберите необходимые настройки.', reply_markup=kb.settings)


@router.callback_query(F.data == 'words_settings')
async def process_words_settings(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите необходимые действия.', reply_markup=kb.words_settings)


@router.callback_query(F.data == 'add_words')
async def process_add_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    added_words = await rq.get_added_user_words(callback.from_user.id)
    first_sentence = f'*Ваши добавленные слова:* _{", ".join(added_words)}_\n\n' if added_words else '*У вас пока нет добавленных слов.*\n\n'

    await state.set_state(AddWords.words)
    await callback.message.edit_text(
        first_sentence + 'Отправьте мне слова, которые нужно добавить в список нецензурных слов.\n',
        parse_mode='Markdown', reply_markup=kb.back_to_word_settings)


@router.callback_query(F.data == 'remove_words')
async def process_remove_words(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')

    removed_words = await rq.get_removed_user_words(callback.from_user.id)
    first_sentence = f'*Ваши удалённые слова:* _{", ".join(removed_words)}_\n\n' if removed_words else '*У вас пока нет удалённых слов.*\n\n'

    await state.set_state(RemoveWords.words)
    await callback.message.edit_text(
        first_sentence + 'Отправьте мне слова, которые нужно удалить из списка нецензурных слов.\n',
        parse_mode='Markdown', reply_markup=kb.back_to_word_settings)


@router.callback_query(F.data == 'back_to_settings')
async def process_back_to_settings(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите необходимые настройки.', reply_markup=kb.settings)


@router.callback_query(F.data == 'back_to_word_settings')
async def process_back_to_word_settings(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите необходимые действия.', reply_markup=kb.words_settings)


@router.callback_query(F.data == 'back_to_start')
async def process_back_to_start(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.delete()
    await callback.message.answer('Выберите пункт меню.', reply_markup=kb.start)


@router.callback_query(F.data == 'words_list')
async def process_words_list(callback: CallbackQuery):
    await callback.answer('')
    message = await callback.message.answer('Собираю список нецензурных слов...')

    words = await rq.get_words(callback.from_user.id)
    file = io.StringIO('\n'.join(words))

    await callback.message.reply_document(document=BufferedInputFile(
        file=file.getvalue().encode('UTF-8'),
        filename='words.txt'
    ), caption='Список нецензурных слов.', reply_markup=kb.start)
    await message.delete()


@router.message(Command('help'))
@router.message(F.text == kb.button_texts['help'])
async def process_help(message: Message):
    await message.answer('Помощь пока не доступна.')


@router.message(ProcessText.text)
async def process_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)

    data = await state.get_data()

    bot_message = await message.answer('Текст обрабатывается...')

    words = await rq.get_words(message.from_user.id)
    text = detox(data['text'], words)

    await bot_message.delete()
    await message.answer(text, reply_markup=kb.start)
    await state.clear()


@router.message(RemoveWords.words)
async def process_remove_words(message: Message, state: FSMContext):
    words = set(message.text.split())

    await rq.set_removed_user_words(message.from_user.id, words)
    await message.answer('Слова удалены.', reply_markup=kb.start)
    await state.clear()


@router.message(AddWords.words)
async def process_add_words(message: Message, state: FSMContext):
    words = set(message.text.split())

    await rq.set_added_user_words(message.from_user.id, words)
    await message.answer('Слова добавлены.', reply_markup=kb.start)
    await state.clear()
