import socket


def find_free_port(
        start_port: int = 8000, host: str = '127.0.0.1',
        max_attempts: int = 100,
        ignore_ports_list: list[int] | None = None,
) -> int:
    """
    Находит первый свободный порт, начиная с start_port
    :param start_port: начальный порт относительно которого будет поиск свободных портов
    :param host: хост, для посторения url
    :param max_attempts: диапазон поиска портов start_port + max_attempts
    :param ignore_ports_list: игнорировать эти порты (иногда сервера ещё не успели запуститься а порт уже занят)
    :return:
    """
    for port in range(start_port, start_port + max_attempts):
        if port in ignore_ports_list:
            continue
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.close()
            return port
        except OSError:
            continue
    raise RuntimeError(f"Не найден свободный порт в диапазоне {start_port}-{start_port + max_attempts - 1}")


if __name__ == '__main__':
    print(find_free_port(start_port=8000, ignore_ports_list=[8000, 8002]))  # 8000
