import logging


class Logger:
    GLOBAL_LOG_FILE = "global.log"  # Общий лог-файл

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)

        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler(f"{name}.log")
            file_handler.setLevel(logging.DEBUG)
            global_handler = logging.FileHandler(Logger.GLOBAL_LOG_FILE)
            global_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            global_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.addHandler(global_handler)

        return logger
