import asyncio
import logging
import signal

from data import States
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    PersistenceInput,
    PicklePersistence,
    filters,
)

from bot import handlers
from src.config import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = settings.app_config.bot.get_token


async def main() -> None:
    """Запуск бота."""
    store_data = PersistenceInput(chat_data=True, user_data=True, bot_data=True)
    persistence = PicklePersistence(
        filepath="databot", store_data=store_data, update_interval=5
    )
    application = (
        Application.builder()
        .token(TOKEN)
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", handlers.start)],
        states={
            States.START.value: [CallbackQueryHandler(handlers.handle_menu_choice)],
            States.QUESTIONS.value: [CallbackQueryHandler(handlers.handle_answer)],
            States.INSTRUCTION.value: [CallbackQueryHandler(handlers.instruction)],
            States.CHOICE_CHILD.value: [
                CallbackQueryHandler(handlers.handle_choice_child)
            ],
            States.ADD_CHILD.value: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, handlers.handle_add_child
                )
            ],
            States.ADD_NAME.value: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, handlers.handle_add_name
                )
            ],
            States.ADD_DATE.value: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, handlers.handle_add_date
                )
            ],
            States.RESULT.value: [
                CallbackQueryHandler(
                    handlers.handle_result, pattern="^(start|history|next)$"
                )
            ],
            States.HISTORY.value: [CallbackQueryHandler(handlers.history)],
            States.ANONYMOUS.value: [CallbackQueryHandler(handlers.anonymous)],
            States.AGE.value: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, handlers.handle_age_text
                )
            ],
        },
        fallbacks=[CommandHandler("start", handlers.start)],
        per_message=False,
        persistent=True,
        name="conversation",
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", handlers.help_command))

    running = True  # определение состояния, что бот работает

    async def shutdown() -> None:
        """Корректное завершение работы"""
        nonlocal running
        if not running:
            return

        running = False
        logger.info("Сохранение данных и остановка бота...")

        try:
            await application.update_persistence()
            if application.running:
                await application.stop()
        except Exception as e:
            logger.error(f"Ошибка при завершении: {e}")
        finally:
            logger.info("Бот остановлен")

    def signal_handler(signum, frame) -> None:  # type: ignore
        logger.info(f"Получен сигнал {signum}, завершение работы...")
        asyncio.create_task(shutdown())

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, signal_handler)

    try:
        logger.info("Запуск бота...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        logger.info("Бот успешно запущен. Ctrl+C для остановки")

        while running:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        await shutdown()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await shutdown()
    finally:
        if running:
            await shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Завершение работы по KeyboardInterrupt")
    except Exception as e:
        logger.error(f"Фатальная ошибка: {e}")
