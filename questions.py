from SQLite import update_quiz_index, get_quiz_index, update_quiz_score, get_quiz_score
from data import quiz_data
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

async def get_question(message, user_id):
    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']
    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, opts[correct_index])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    score = 0
    current_question_index = 0
    await update_quiz_score(user_id, score)
    await update_quiz_index(user_id, current_question_index)
    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)

def generate_options_keyboard(answer_options, right_answer):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()
    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options:
        if option == right_answer:
            check_answer="right_answer"  + '|' + f'{option}'
        else:
            check_answer="wrong_answer" + '|' + f'{option}'
        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right_answer'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong_answer'
            callback_data=check_answer)
        )
    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()
