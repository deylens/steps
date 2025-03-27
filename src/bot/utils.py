from telegram import Update


def update_skill(data: dict, current_question: int, approve: str) -> dict:
    """
    Сохранение ответов в промежуточном словаре
    Args: data: список с вопросами, current_questions:  текст вопроса, approve: ответ вопроса

    Return: data: промежуточный список с ответами на вопрос
    """

    if approve == "Освоил":
        data["questions"][current_question]["approve"] = True
    else:
        data["questions"][current_question]["approve"] = False
    return data


def get_child_data(data: dict) -> list:
    """
    Получение списка для клавиатуры бота
    Args: список детей пользователя

    return: список детей для клавиатуры бота

    """
    child_list = []
    for i in range(len(data["child"])):
        name = data["child"][i]["name"]
        date = data["child"][i]["date"]
        current_child = f"{name} {date}"
        child_list.append(current_child)
    return child_list


def get_recommendation(data: dict) -> list:
    """
    Получение рекомендаций в зависимости от ответов
    Args: промежуточный список с вопросами и ответами

    Return: список словарей, с ответами False
    """
    _recom_list = []

    # Итерируемся по вопросам
    for recom in data["questions"]:
        if not recom["approve"]:
            _recom_dict = {
                "name": recom["name"],
                "recommendation": recom["recommendation"],
            }
            _recom_list.append(_recom_dict)

    return _recom_list


async def get_message(update: Update) -> Update:
    if update.message:
        return update.message
    elif update.callback_query and update.callback_query.message:
        return update.callback_query.message
    else:
        raise ValueError("Не удалось получить объект сообщения")


async def error_message(update: Update) -> Update:
    """
    Сообщение пользователю об ошибке при взаиможействии с ботом

    Args: Update из telegram.ext
    """
    try:
        if update.callback_query:
            await update.callback_query.answer("Произошла ошибка, попробуйте еще раз")
        if update.message:
            await update.message.reply_text("Произошла ошибка, попробуйте еще раз")
    except:
        pass
