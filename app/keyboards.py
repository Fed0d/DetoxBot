from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

button_texts = {
    'process_text': 'Обработать текст 📝',
    'settings': 'Настройки ⚙️',
    'help': 'Помощь ❓'
}

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=button_texts['process_text'])],
    [KeyboardButton(text=button_texts['settings']), KeyboardButton(text=button_texts['help'])]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню.')
