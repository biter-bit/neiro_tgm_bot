import logging
from logging import Logger
from config import settings
import os


def create_logger(level_logger: str) -> Logger:
    """Создай логер"""
    basic_path = os.path.join(settings.PATH_WORK, 'logs')
    print(basic_path)

    log_format = "%(asctime)s [%(levelname)s] [%(name)s] [%(threadName)s] [%(filename)s:%(lineno)d] - %(message)s"

    logging.basicConfig(level=getattr(logging, level_logger.upper()), format=log_format)

    logger = logging.getLogger("my_logger")
    logger.setLevel(getattr(logging, level_logger.upper()))

    # Создание файлового обработчика для обычных логов
    file_handler = logging.FileHandler(os.path.join(basic_path, 'app.log'))
    file_handler.setLevel(logging.INFO)  # Логи от INFO и выше
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    # Создание файлового обработчика для ошибок
    error_handler = logging.FileHandler(os.path.join(basic_path, 'errors.log'))
    error_handler.setLevel(logging.ERROR)  # Логи только для ошибок
    error_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(error_handler)

    return logger