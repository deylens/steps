import logging
from typing import Any

from data import DATA, TEXT, States
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, error
from telegram.ext import ContextTypes
from utils import (
    birth_date,
    error_message,
    get_child_data,
    get_message,
    get_recommendation,
    update_skill,
)

from src.dependencies import (
    get_child_service,
    get_diagnosis_service,
    get_recommendation_service,
    get_user_repository,
    get_user_service,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Начало диалога и вывод меню.

    """
    try:
        message = update.message or update.callback_query.message
        service = get_user_service()
        context.user_data.update(
            {
                "user": None,
                "current_questions": 0,
                "is_anonymous": False,
                "children": None,
                "current_child": None,
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


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Вопросы из списка SKILL.

    """
    try:
        message = await get_message(update)
        current_question = context.user_data.get("current_questions", 0)
        service = get_diagnosis_service()
        questions = service.start_diagnosis(context.user_data["current_child"])
        context.user_data["questions"] = questions

        if current_question < len(questions):
            skill = questions[current_question]
            print(skill)
            await message.reply_text(
                text=f" skill {skill.criteria}, skill_id {skill.id} skill_type {skill.skill_type_id}, age_start {skill.age_start} age {skill.age_actual}",
                reply_markup=build_keyboard(["Выполнил", "Не выполнил"]),
            )

            return States.QUESTIONS
        else:
            return await result(update, context)
    except Exception as e:
        logging.info(f"error {e}")
        await message.reply_text(f"Произошла ошибка, возвращаюсь к начальной странице")
        return await start(update, context)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    """
    Обрабатывает ответ пользователя на вопрос.

    """
    answer_data = {"Выполнил": True, "Не выполнил": False}
    query = update.callback_query
    try:
        await query.answer()
    except error.BadRequest as e:
        if "Query is too old" in str(e):
            logging.warning(f"Expire callback: {e}")
    user_answer = query.data
    service = get_diagnosis_service()
    questions = context.user_data["questions"]
    child_id = context.user_data["current_child"]
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


async def result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    message = await get_message(update)
    service = get_diagnosis_service()
    child_id = context.user_data["current_child"]
    result = service._get_diagnosis_results(child_id=child_id)
    service.save_diagnosis(child_id=child_id, result=result)
    finish_result = service.finish_diagnosis(child_id=child_id)
    logging.info(f"{finish_result}")
    if "current_recommend_index" not in context.user_data:
        context.user_data["current_recommend_index"] = 0

    current_index = context.user_data.get("current_recommend_index", 0)
    recommend = finish_result["skill_mastered"]
    keyboard = [
        InlineKeyboardButton("История", callback_data="history"),
        InlineKeyboardButton("Старт", callback_data="start"),
    ]
    logging.info(recommend.items())
    if current_index == 0:
        await message.reply_text(text="Идёт подсчёт результата")

    if current_index < len(recommend.items()):
        item = list(recommend.items())[current_index]
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


def build_keyboard(  # type: ignore
    current_list: list[str], callback_data=None, **kwargs: Any
) -> InlineKeyboardMarkup:
    """Создает клавиатуру с вариантами ответов.

    Args:
        current_list: Список текстов кнопок или кортежей (текст, значение)
        callback_data: Базовый callback_data (если не используется список кортежей)
        **kwargs: Дополнительные параметры (будут добавлены в callback_data через ";")
    """

    buttons = []

    for item in current_list:
        # Определяем текст кнопки и значение для callback_data
        if isinstance(item, tuple) and len(item) == 2:
            text, value = item
        else:
            text = value = item

        # Формируем основной callback_data
        cb_data = str(value) if callback_data is None else callback_data

        # Добавляем kwargs если они есть
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
