import requests
from time import time, sleep


class ServerProbe:
    """
    Набор утилит для опроса сервера.
    Например проверка что сервер запущен, или наоборот что сервер остановлен.
    """

    @staticmethod
    def wait_for_server_up(
            url: str,
            timeout: float = 5,
            interval: float = 0.3,
            expected_status: int = 200,
    ) -> None:
        """
        Проверка что сервер запущен. Опрос его timeout времени, с шагом interval.
        :param url: url
        :param timeout: время ожидания
        :param interval: интервал между запросами
        :param expected_status: ожидаемый статус код от сервера (обычно 200)
        :return: None -> возбуждает исключение если сервер не запустился за timeout время
        """
        deadline = time()
        while time() - deadline < timeout:
            try:
                res = requests.get(url, timeout=1)
                if res.status_code == expected_status:
                    print(f'✅ Сервер `{url}` запущен')
                    return None
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.RequestException:
                pass
            sleep(interval)

        raise TimeoutError(f'Превышено время ожидания для `{url}`')

    @staticmethod
    def wait_for_server_down(url: str, timeout: float = 5, interval: float = 0.3):
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
                requests.get(url, timeout=1)
            except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
                print(f'✅ Сервер `{url}` остановлен.')
                return
            sleep(interval)
        raise TimeoutError(f'Сервер `{url}` не остановился за {timeout} сек.')
