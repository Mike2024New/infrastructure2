from __future__ import annotations

import warnings
import loguru
from loguru import logger
from pathlib import Path

__all__ = ['Logger']


class Logger:
    def __init__(
            self, log_path: Path,
            rotation: str = '10 MB', retention: int = 10,
            compression: str = 'zip',
            fmt: str = '{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[request_id]} | {message}'
    ):
        # добавить по умолчанию чтобы логер в библиотеках не ругался на отсутствие request_id
        logger.configure(extra={"request_id": "N/A"})
        self.logger: loguru.Logger | None = None
        self._log_path = log_path
        self._rotation = rotation
        self._retention = retention
        self._compression = compression
        self._fmt = fmt
        self._handler_added = False

    def set_logger(self, request_id: str):
        """Общий логгер на всё приложение с фиксированным request_id для отслеживания всёй цепочки"""
        self._log_path.parent.mkdir(exist_ok=True, parents=True)
        if self.logger is None:
            logger.add(
                self._log_path,
                rotation=self._rotation, retention=self._retention,
                compression=self._compression,
                format=self._fmt,
            )
            self.logger = logger.bind(request_id=request_id)
        else:
            warnings.warn(f'Попытка установить логгер второй раз')

    # набор прокси методов для удобства
    def info(self, msg: str, *args, **kwargs):
        self._ensure_logger().info(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self._ensure_logger().error(msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self._ensure_logger().debug(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self._ensure_logger().warning(msg, *args, **kwargs)

    def success(self, msg: str, *args, **kwargs):
        self._ensure_logger().success(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self._ensure_logger().critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        self._ensure_logger().exception(msg, *args, **kwargs)

    def opt(self, *args, **kwargs) -> loguru.Logger:
        """Прокси для logger.opt (возвращает логгер для цепочки вызовов)"""
        return self._ensure_logger().opt(*args, **kwargs)

    def _ensure_logger(self) -> loguru.Logger:
        """Вспомогательный метод для проверки, что логгер инициализирован"""
        if self.logger is None:
            if not self._handler_added:
                logger.add(
                    self._log_path,
                    rotation=self._rotation, retention=self._retention,
                    compression=self._compression,
                    format=self._fmt,
                )
                self._handler_added = True
            self.logger = logger.bind(request_id='N/A')
            warnings.warn("Логгер инициализирован без request id.")
        return self.logger

    def catch(self, *args, **kwargs):
        """Прокси для logger.catch"""
        return self._ensure_logger().catch(*args, **kwargs)


if __name__ == '__main__':
    """Пример использования"""
    log = Logger(
        log_path=Path.cwd() / 'logs/app.log'
    )


    # для сквозных логов не использовать catch, так как он не работает до инициализации
    def x():
        try:
            print(1 / 0)
        except Exception as err:
            log.exception(f'{err}')  # чтобы была трассировка использ. exception


    # log.set_logger(request_id='#001')
    x()
    log.info('test')
