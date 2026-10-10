from datetime import datetime


class TimeUtils:
    """Класс с набором утилит, для времени. Удобство в задании общего формата в инициализаторе"""

    def __init__(self, timestamp_fmt: str = '%d.%m.%Y %H:%M:%S.%f'):
        self._timestamp_fmt = timestamp_fmt

    def timestamp(self, fmt: str | None = None):
        """Получение текущего времени в заданном формате"""
        if fmt is not None:
            return datetime.now().strftime(fmt)
        return datetime.now().strftime(self._timestamp_fmt)


if __name__ == '__main__':
    time_utils = TimeUtils(timestamp_fmt='%d.%m.%Y')  # централизованно определяется формат
    print(time_utils.timestamp())  # формат един для всех вызовов
    print(time_utils.timestamp())  # формат един для всех вызовов
    print(time_utils.timestamp(fmt='%d.%m.%Y %H:%M:%S.%f'))  # точечно переопределен
