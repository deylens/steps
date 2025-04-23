import logging
from collections.abc import Callable
from datetime import date
from functools import wraps
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def update_skill(data: dict, current_question: int, approve: str) -> dict:
    """
    Сохранение ответов в промежуточном словаре
    Args:
        data: список с вопросами,
        current_questions:  текст вопроса, approve: ответ вопроса

    Return:
        data: промежуточный список с ответами на вопрос
    """

    if approve == "Освоил":
        data["questions"][current_question]["approve"] = True
    else:
        data["questions"][current_question]["approve"] = False
    return data


def get_child_data(data: dict) -> list:
    """
    Получение списка для клавиатуры бота
    Args:
        data : список детей пользователя

    return:
        data: список детей для клавиатуры бота

    """
    child_list = []
    for child in data:
        name = child.name
        date = child.birth_date
        current_child = f"{name} {date}"
        child_list.append(current_child)
    return child_list


def get_recommendation(data: dict) -> list:
    """
    Получение рекомендаций в зависимости от ответов
    Args:
        data: промежуточный список с вопросами и ответами

    Return:
        data: список словарей, с ответами False
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


def birth_date(user_date: str) -> date:
    input_data = "-".join(user_date.split(".")[::-1])
    output_data = date.fromisoformat(input_data)
    return output_data


def log_handler_errors(handler_func: Callable) -> Callable:
    """
    Декоратор для логирования ошибок в обработчиках python-telegram-bot.
    Логирует:
    - Начало выполнения обработчика
    - Успешное завершение
    - Возникшие ошибки
    """

    @wraps(handler_func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        handler_name = handler_func.__name__

        try:
            logger.info(f"Обработчик '{handler_name}' начал выполнение")
            result = await handler_func(update, context)
            logger.info(f"Обработчик '{handler_name}' успешно завершился")
            return result

        except Exception as e:
            logger.error(
                f"Ошибка в обработчике '{handler_name}': {str(e)}",
                exc_info=True,  # Добавляет traceback в лог
            )
            await error_message(update)  # Ваша функция для отправки сообщения об ошибке
            return ConversationHandler.START  # Или другой подходящий fallback

    return wrapper
