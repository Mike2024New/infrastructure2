import sys, subprocess, threading, signal, os
from pathlib import Path

"""
Простой менеджер для завершения процессов, которые не были уничтожены при закрытии программы
(например грубое закрытие терминала).
"""


class PidManager:
    def __init__(self, pid_file_path: Path):
        """
        :param pid_file_path: путь к файлу. Например `projects/pid.txt`
        """
        self._pid_file_path = pid_file_path
        if not self._pid_file_path.exists():
            self._pid_file_path.write_text('', encoding='utf8')  # создание файла если его ещё нет
        self._lock = threading.Lock()

    @staticmethod
    def _kill_pid(pid: int):
        """Принудительная остановка процессов"""
        if sys.platform == 'win32':
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True, shell=True)
        else:
            os.kill(pid, signal.SIGTERM)

    def add(self, pid: int):
        """Добавление pid в файл с процессами"""
        with self._lock:
            with open(file=self._pid_file_path, mode='a', encoding='utf8') as f:
                f.write(f'{pid}\n')

    def stop(self):
        """Остановка не завершенных процессов (те которые есть в файле pid.txt)"""
        with self._lock:
            with open(file=self._pid_file_path, mode='r', encoding='utf8') as f:
                pids = f.read().splitlines()
                for pid in pids:
                    self._kill_pid(pid=int(pid))
        self.clear()  # очистка файла завершенных процессов

    def clear(self):
        """Очистка файла с pid"""
        with self._lock:
            with open(file=self._pid_file_path, mode='w', encoding='utf8') as f:
                f.write('')
