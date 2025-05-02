import logging
from datetime import date
from typing import Any

from data import TEXT, States
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, error
from telegram.ext import ContextTypes
from utils import (
    birth_date,
    error_message,
    get_message,
    log_handler_errors,
)

from src.dependencies import (
    get_child_service,
    get_diagnosis_service,
    get_recommendation_service,
    get_user_service,
)


@log_handler_errors
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Start a dialogue and display a menu.

    """
    try:
        message = update.message or update.callback_query.message
        service = get_user_service()
        context.user_data.update(
            {
                "user": None,
                "current_questions": 0,
                "children": None,
                "current_child": None,
                "current_date": None,
            }
        )
        telegram_id = update.effective_user.id
        user = service.get_user_by_telegram_id(telegram_id=telegram_id)
        context.user_data["user"] = user
        if user:
            username = update.effective_user.full_name
            await message.reply_text(f"Привествуем,{username}")
            await message.reply_text(TEXT["greetings"])
        else:
            user = service.register_user(telegram_id=telegram_id)
            context.user_data["user"] = user
            await message.reply_text(
                f"{update.effective_user.full_name}, Вы зарегистрированы"
            )

        menu_keyboard = ["Инструкция", "Диагностика"]

        await message.reply_text(
            "Пожалуйста, выберите:", reply_markup=build_keyboard(menu_keyboard)
        )

        return States.START

    except Exception as error:
        logging.error(f"Error in start is {error}")
        await error_message(update)
    return States.START.value


@log_handler_errors
async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Processing user selection in the menu.

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


@log_handler_errors
async def choice_child(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Child selection menu

    """
    query = update.callback_query
    await query.answer()
    service = get_child_service()
    children = service.get_children(context.user_data["user"].id)
    keyboard = ["Выбрать", "Добавить"] if len(children) > 0 else ["Добавить"]
    await query.edit_message_text(
        text="Выберете или добавьте данные ребенка:",
        reply_markup=build_keyboard(keyboard),
    )

    return States.CHOICE_CHILD


@log_handler_errors
async def handle_choice_child(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Any:
    """
    Processing child selection in the menu.

    """
    query = update.callback_query
    service = get_child_service()
    await query.answer()
    choice = query.data

    if choice == "Добавить":
        return await handle_add_child(update, context)

    elif choice == "Выбрать":
        children = service.get_children(context.user_data["user"].id)

        buttons = [
            InlineKeyboardButton(
                text=f"{child.name} ({child.birth_date})",
                callback_data=child.id,
            )
            for child in children
        ]

        await query.edit_message_text(
            text="Выберите ребенка из списка:",
            reply_markup=InlineKeyboardMarkup([buttons]),
        )
        return States.CHOICE_CHILD

    elif type(choice) == int:
        child_id = choice
        context.user_data["current_child"] = child_id
        context.user_data["current_questions"] = 0

        return await ask_question(update, context)


@log_handler_errors
async def handle_add_child(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Adding child's name

    """
    context.user_data["child"] = {}
    query = update.callback_query
    await query.edit_message_text(text="Введите имя ребенка")

    return States.ADD_NAME


@log_handler_errors
async def handle_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Processing adding child's name

    """
    user_input = update.message.text
    context.user_data["child"]["name"] = user_input
    await update.message.reply_text(
        "Введите дату рождения ребенка в формате ДД.ММ.ГГГГ"
    )

    return States.ADD_DATE


@log_handler_errors
async def handle_add_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Adding child's birth date

    """
    service = get_child_service()
    user_input = update.message.text
    context.user_data["child"]["date"] = birth_date(user_input)
    service.add_child(
        user_id=context.user_data["user"].id,
        name=context.user_data["child"]["name"],
        birth_date=context.user_data["child"]["date"],
    )

    if update.message:
        await update.message.reply_text(
            f"Ребенок {context.user_data['child']['name']} с датой {context.user_data['child']['date']} добавлен"
        )
    else:
        await update.callback_query.message.reply_text(
            f"Ребенок {context.user_data['child']['name']} с датой {context.user_data['child']['date']} добавлен"
        )

    context.user_data["current_questions"] = 0
    context.user_data["child"] = {}

    keyboard = ["Выбрать", "Добавить"]
    await update.message.reply_text(
        text="Выберите действие:", reply_markup=build_keyboard(keyboard)
    )

    return States.CHOICE_CHILD


@log_handler_errors
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Output of questions by list and get answer

    """
    try:
        message = await get_message(update)
        current_question = context.user_data.get("current_questions", 0)
        service = get_diagnosis_service()
        questions = service.start_diagnosis(context.user_data["current_child"])
        context.user_data["questions"] = questions

        if current_question < len(questions):
            skill = questions[current_question]
            await message.reply_text(
                text=f" {skill.criteria}",
                reply_markup=build_keyboard(["Выполнил", "Не выполнил"]),
            )

            return States.QUESTIONS
        else:
            return await result(update, context)
    except Exception as e:
        logging.info(f"error {e}")
        await message.reply_text(f"Произошла ошибка, возвращаюсь к начальной странице")
        return await start(update, context)


@log_handler_errors
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Processing the answer to the questions

    """
    try:
        query = update.callback_query
        await query.answer()

        child_id = context.user_data["current_child"]
        if not child_id:
            await query.message.reply_text("Сессия устарела, возвращаемся к началу")
            return await start(update, context)

        answer_data = {"Выполнил": True, "Не выполнил": False}
        user_answer = query.data

        if user_answer not in answer_data:
            logging.warning(f"Неожиданный ответ - {user_answer}")
            await query.message.reply_text(
                "Ошибка в получении ответа, возвращаемся к вопросу"
            )
            return await ask_question(update, context)
        service = get_diagnosis_service()
        questions = context.user_data["questions"]
        if not questions:
            query.message.reply_text(
                "Ошибка в формировании вопросов, возвращаемся к началу"
            )
            return await start(update, context)

        current_question = context.user_data.get("current_questions", 0)
        answer = answer_data[user_answer]
        service.submit_question(
            child_id=child_id,
            skill_id=questions[current_question].id,
            skill_type=questions[current_question].skill_type_id,
            answer=answer,
        )
        context.user_data["current_questions"] += 1
        return await ask_question(update, context)

    except error.BadRequest as e:
        if "Query is too old" in str(e):
            logging.warning(f"Expire callback: {e}")


@log_handler_errors
async def instruction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Output istructions

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


@log_handler_errors
async def result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Result output from user's poll

    """
    try:
        message = await get_message(update)
        service = get_diagnosis_service()
        child_id = context.user_data["current_child"]
        current_date: date = date.today()
        if not child_id:
            await message.reply_text("Ребенок не найден, вернёмся к началу")
            return await start(update, context)
        result = service._get_diagnosis_results(child_id=child_id)
        service.save_diagnosis(child_id=child_id, result=result)
        recommendations = list(
            get_recommendation_service().get_recommendations(
                child_id=child_id, date=current_date
            )
        )
        logging.info(recommendations)

        if not recommendations:
            await message.reply_text("Рекомендации не найдены")
            return States.RESULT

        if "current_recommend_index" not in context.user_data:
            context.user_data["current_recommend_index"] = 0

        current_index = context.user_data.get("current_recommend_index", 0)
        keyboard = [
            InlineKeyboardButton("История", callback_data="history"),
            InlineKeyboardButton("Старт", callback_data="start"),
        ]

        if current_index == 0:
            await message.reply_text(text="Идёт подсчёт результата")

        if current_index < len(recommendations):
            item = recommendations[current_index]
            await message.reply_text(
                f"{item}",
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
    except Exception as e:
        logging.error(f"Error in result is {e}")
        await error_message(update)
        return await start(update, context)


@log_handler_errors
async def handle_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Processing result selections

    """
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


# TODO
@log_handler_errors
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Output history of polls

    """
    query = update.callback_query
    keyboard = ["Назад"]
    await query.edit_message_text(
        text=TEXT["history"], reply_markup=build_keyboard(keyboard)
    )

    if query.data == "Назад":
        await start(update, context)
        return States.START

    return States.HISTORY


def build_keyboard(  # type: ignore
    current_list: list[str], callback_data=None, **kwargs: Any
) -> InlineKeyboardMarkup:
    """
    Create keyboard with selection choice

    Args:
        current_list: list text buttons or tuple (text, value)
        callback_data: Basic callback_data (without current_list in Args)
        **kwargs: Extra params (add in callback_data across ";")
    """

    buttons = []

    for item in current_list:
        if isinstance(item, tuple) and len(item) == 2:
            text, value = item
        else:
            text = value = item

        cb_data = str(value) if callback_data is None else callback_data

        if kwargs:
            kwargs_str = ";".join(f"{k}={v}" for k, v in kwargs.items())
            cb_data = f"{cb_data};{kwargs_str}"

        buttons.append(InlineKeyboardButton(text, callback_data=cb_data))

    return InlineKeyboardMarkup.from_row(buttons)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""

    await update.message.reply_text(
        "Use /start to test this bot. Use /clear to clear the stored data so that you can see "
        "what happens, if the button data is not available. "
    )
