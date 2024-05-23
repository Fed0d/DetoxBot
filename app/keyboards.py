from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

button_texts = {
    'process_text': 'Обработать текст 📝',
    'settings': 'Настройки ⚙️',
    'help': 'Помощь ❓',
    'words_settings': 'Настройки списка нецензурных слов 🤬',
    'add_words': 'Добавить слова 🟢',
    'remove_words': 'Удалить слова 🔴',
    'back': 'Назад ↩️',
    'words_list': 'Список слов 📜'
}

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=button_texts['process_text'])],
    [KeyboardButton(text=button_texts['settings']), KeyboardButton(text=button_texts['help'])]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.')

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=button_texts['words_settings'], callback_data='words_settings')]
])

words_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=button_texts['add_words'], callback_data='add_words'),
     InlineKeyboardButton(text=button_texts['remove_words'], callback_data='remove_words')],
    [InlineKeyboardButton(text=button_texts['words_list'], callback_data='words_list')],
    [InlineKeyboardButton(text=button_texts['back'], callback_data='back_to_settings')]
])

back_to_word_settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=button_texts['back'], callback_data='back_to_word_settings')]
])

back_to_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=button_texts['back'], callback_data='back_to_start')]
])
