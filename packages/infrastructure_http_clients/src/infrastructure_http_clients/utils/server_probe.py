import requests
from time import time, sleep


class ServerProbe:
    """
    Набор утилит для опроса сервера.
    Например проверка что сервер запущен, или наоборот что сервер остановлен.
    """

    @classmethod
    def polling(
            cls,
            url: str,
            timeout: float = 5,
            interval: float = 0.3,
            expected_status: int = 200,
            **kwargs,
    ) -> requests.Response | None:
        """
        Поллинг сервера. Опрос его timeout времени, с шагом interval. (Нужно учитывать rate limit, или делать long polling)
        возвращает response сервера
        (Дублирует логику wait_for_server_up, так как название polling удобнее)
        :param url: url
        :param timeout: время ожидания
        :param interval: интервал между запросами
        :param expected_status: ожидаемый статус код от сервера (обычно 200)
        :return: None -> возбуждает исключение если сервер не запустился за timeout время
        """
        return cls.wait_for_server_up(url, timeout, interval, expected_status, **kwargs)

    @staticmethod
    def wait_for_server_up(
            url: str,
            timeout: float = 5,
            interval: float = 0.3,
            expected_status: int = 200,
            **kwargs,
    ) -> requests.Response | None:
        """
        Проверка что сервер запущен. Опрос его timeout времени, с шагом interval.
        возвращает response сервера
        :param url: url
        :param timeout: время ожидания
        :param interval: интервал между запросами
        :param expected_status: ожидаемый статус код от сервера (обычно 200)
        :return: None -> возбуждает исключение если сервер не запустился за timeout время
        """
        deadline = time()
        while time() - deadline < timeout:
            try:
                res = requests.get(url, timeout=1, **kwargs)
                if res.status_code == expected_status:
                    return res
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.RequestException:
                pass
            sleep(interval)

        raise TimeoutError(f'Превышено время ожидания для `{url}`')

    @staticmethod
    def wait_for_server_down(
            url: str,
            timeout: float = 5,
            interval: float = 0.3,
            **kwargs,
    ) -> None:
        """
        Проверка что сервер завершил работу. Опрос его timeout времени, с шагом interval.
        :param url: url
        :param timeout: время ожидания
        :param interval: интервал между запросами
        :return: None -> возбуждает исключение если сервер выдает 200 спустя заданное timeout время
        """
        deadline = time()
        while time() - deadline < timeout:
            try:
                requests.get(url, timeout=1, **kwargs)
            except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
                return
            sleep(interval)
        raise TimeoutError(f'Сервер `{url}` не остановился за {timeout} сек.')
