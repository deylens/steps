import logging
from collections.abc import Callable
from datetime import date
from functools import wraps
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

from src.bot.data import States

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def get_message(update: Update) -> Update:
    if update.message:
        return update.message
    elif update.callback_query and update.callback_query.message:
        return update.callback_query.message
    else:
        raise ValueError("Не удалось получить объект сообщения")


async def error_message(update: Update) -> Update:
    """
    Message for users about some error

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
    Decorator for logging errors to handlers
    Logs:
    - Start work handler
    - Success work
    - Raise errors
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
                exc_info=True,
            )
            await error_message(update)
            return States.START

    return wrapper
