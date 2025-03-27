import logging
from typing import Any

from data import DATA, TEXT, States
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import (
    error_message,
    get_child_data,
    get_message,
    get_recommendation,
    update_skill,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Начало диалога и вывод меню.

    """
    try:
        message = update.message or update.callback_query.message
        context.user_data.update({"current_questions": 0, "is_anonymous": False})
        if DATA["id_user"] == None or "id_user" not in DATA:
            DATA["id_user"] = update.effective_user.id
            await message.reply_text(TEXT["greetings"])
        else:
            username = update.effective_user.full_name
            await message.reply_text(f"Hello,{username}")

        menu_keyboard = ["Инструкция", "Диагностика", "Анонимно"]

        await message.reply_text(
            "Пожалуйста, выберите:", reply_markup=build_keyboard(menu_keyboard)
        )

        return States.START

    except Exception as error:
        logging.error(f"Error in start is {error}")
        await error_message(update)
    return States.START.value


async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Обработка выбора пользователя в меню.

    """

    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "Диагностика":
        return await choice_child(update, context)

    elif choice == "Инструкция":
        return await instruction(update, context)

    elif choice == "Назад":
        return States.START

    elif choice == "Анонимно":
        context.user_data["is_anonymous"] = True
        await query.message.reply_text(f"{TEXT['anonymous']}")
        return await anonymous(update, context)


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Вопросы из списка SKILL.

    """

    message = await get_message(update)
    current_question = context.user_data.get("current_questions", 0)

    if current_question < len(DATA["questions"]):
        skill = DATA["questions"][current_question]

        await message.reply_text(
            text=f"{skill['name']}: {skill['creteria']}",
            reply_markup=build_keyboard(["Освоил", "Не освоил"]),
        )

        return States.QUESTIONS
    else:
        return await result(update, context)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Обрабатывает ответ пользователя на вопрос.

    """
    query = update.callback_query
    await query.answer()
    user_answer = query.data

    if user_answer in ["Освоил", "Не освоил"]:
        current_question = context.user_data.get("current_questions", 0)
        update_skill(DATA, current_question, user_answer)
        context.user_data["current_questions"] += 1
        return await ask_question(update, context)

    return await ask_question(update, context)


async def instruction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Обработчик для инструкции.

    """
    query = update.callback_query
    keyboard = ["Назад"]

    await query.edit_message_text(
        text=TEXT["instruction"], reply_markup=build_keyboard(keyboard)
    )

    if query.data == "Назад":
        await start(update, context)
        return States.START

    return States.INSTRUCTION


async def choice_child(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()
    keyboard = ["Выбрать", "Добавить"]
    await query.edit_message_text(
        text="Выберете или добавьте данные ребенка:",
        reply_markup=build_keyboard(keyboard),
    )

    return States.CHOICE_CHILD


async def handle_choice_child(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Any:
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "Добавить":
        return await handle_add_child(update, context)

    elif choice == "Выбрать":
        keyboard = get_child_data(DATA)
        await query.edit_message_text(
            text="Выберете ребенка из списка:",
            reply_markup=build_keyboard(keyboard, callback_data="Диагностика"),
        )
        context.user_data["current_questions"] = 0

        return States.QUESTIONS


async def handle_add_child(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    context.user_data["child"] = {}
    query = update.callback_query
    await query.edit_message_text(text="Введите имя ребенка")

    return States.ADD_NAME


async def handle_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    user_input = update.message.text
    context.user_data["child"]["name"] = user_input
    await update.message.reply_text(
        "Введите дату рождения ребенка в формате ДД.ММ.ГГГГ"
    )

    return States.ADD_DATE


async def handle_add_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    user_input = update.message.text
    context.user_data["child"]["date"] = user_input

    if update.message:
        await update.message.reply_text(
            f"Ребенок {context.user_data['child']['name']} с датой {context.user_data['child']['date']} добавлен"
        )
    else:
        await update.callback_query.message.reply_text(
            f"Ребенок {context.user_data['child']['name']} с датой {context.user_data['child']['date']} добавлен"
        )

    if "child" not in DATA:
        DATA["child"] = []
    DATA["child"].append(context.user_data["child"])

    context.user_data["current_questions"] = 0
    context.user_data["child"] = {}

    keyboard = ["Выбрать", "Добавить"]
    await update.message.reply_text(
        text="Выберите действие:", reply_markup=build_keyboard(keyboard)
    )

    return States.CHOICE_CHILD


async def result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    message = await get_message(update)
    if "current_recommend_index" not in context.user_data:
        context.user_data["current_recommend_index"] = 0

    current_index = context.user_data["current_recommend_index"]
    recommend = get_recommendation(DATA)
    keyboard = [
        InlineKeyboardButton("История", callback_data="history"),
        InlineKeyboardButton("Старт", callback_data="start"),
    ]

    if current_index == 0:
        await message.reply_text(text="Идёт подсчёт результата")

    if len(recommend) == 0:
        await message.reply_text(
            "Психо-физическое развитие соответствует возрасту. Опрос завершен.",
            reply_markup=InlineKeyboardMarkup.from_row(keyboard),
        )
        return States.RESULT

    if current_index < len(recommend):
        await message.reply_text(
            f"{recommend[current_index]['name']}\n"
            f"{recommend[current_index]['recommendation']}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Продолжить", callback_data="next")]]
            ),
        )
        context.user_data["current_recommend_index"] += 1

    else:
        await message.reply_text(
            text=f"Опрос завершен. Спасибо!",
            reply_markup=InlineKeyboardMarkup.from_row(keyboard),
        )
        context.user_data["current_recommend_index"] = 0
        return States.RESULT

    return States.RESULT


async def handle_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "next":
        return await result(update, context)

    elif choice == "history":
        return await history(update, context)

    elif choice == "start":
        return await start(update, context)

    else:
        return States.RESULT


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    keyboard = ["Назад"]
    await query.edit_message_text(
        text=TEXT["history"], reply_markup=build_keyboard(keyboard)
    )

    if query.data == "Назад":
        await start(update, context)
        return States.START

    return States.HISTORY


async def anonymous(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Обработчик для анонимного опроса

    """
    message = await get_message(update)
    await message.reply_text("Введите возраст ребенка в годах и месяцах, к примеру 1,5")
    return States.AGE


async def handle_age_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Получаем возраст для анонимного опроса

    """
    message = await get_message(update)
    user_input = message.text
    context.user_data.update({"age": user_input, "current_questions": 0})

    return await ask_question(update, context)


def build_keyboard(current_list: list, callback_data=None) -> InlineKeyboardMarkup:  # type: ignore
    """Создает клавиатуру с вариантами ответов."""
    if callback_data:
        return InlineKeyboardMarkup.from_row(
            [
                InlineKeyboardButton(current_list[i], callback_data=callback_data)
                for i in range(len(current_list))
            ]
        )

    return InlineKeyboardMarkup.from_row(
        [
            InlineKeyboardButton(current_list[i], callback_data=current_list[i])
            for i in range(len(current_list))
        ]
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""

    await update.message.reply_text(
        "Use /start to test this bot. Use /clear to clear the stored data so that you can see "
        "what happens, if the button data is not available. "
    )
