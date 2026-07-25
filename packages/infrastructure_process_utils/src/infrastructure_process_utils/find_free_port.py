import socket
def find_free_port(start_port=8000, max_attempts=100, host='127.0.0.1'):
    """Находит первый свободный порт, начиная с start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.close()
            return port
        except OSError:
            continue
    raise RuntimeError(f"Не найден свободный порт в диапазоне {start_port}-{start_port + max_attempts - 1}")
