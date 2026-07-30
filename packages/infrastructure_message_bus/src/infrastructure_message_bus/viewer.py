import json
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

"""
Быстрый просмотрщик логов для десктопных приложений.

- Работает без внешних зависимостей
- Встроен в .exe сборку
- Позволяет фильтровать по trace_id, component, request_id
- Автоматическое выравнивание колонок

Для крупных систем с сотнями сервисов рекомендуется использовать 
ELK или Grafana Loki.
"""

__all__ = ['LogViewer', 'LogViewerConfig', 'Filters', 'SearchFilters']


# ============ Конфигурация ============
@dataclass(frozen=True)
class Filters:
    """Доступные поля для фильтрации"""
    trace_id: str = 'trace_id'
    request_id: str = 'request_id'
    date: str = 'date'
    component: str = 'component'
    component_id: str = 'component_id'
    subcomponent: str = 'subcomponent'
    level: str = 'level'
    message: str = 'message'
    event: str = 'event'
    error: str = 'error'
    result: str = 'result'
    data: str = 'data'

    @classmethod
    def all_keys(cls) -> list[str]:
        """Получить все ключи"""
        return list(cls().__dict__.values())


@dataclass
class SearchFilters:
    trace_id: str | None = None
    request_id: str | None = None
    component: str | None = None


@dataclass
class LogViewerConfig:
    """Конфигурация просмотрщика логов"""
    root_path: Path
    only_keys: list[str] | None = None
    exclude_dirs: list[str] | None = field(default_factory=lambda: [
        '.venv', '__pycache__', '.git', '.pytest_cache'
    ])
    search_filters: SearchFilters | None = field(default_factory=lambda: SearchFilters())
    log_pattern: str = 'log*.jsonl'
    date_format: str = '%H:%M:%S.%f %d.%m.%Y'
    separator: str = '  |  '  # Разделитель колонок


# ============ Основной класс ============
class LogViewer:
    """Легковесный просмотрщик логов с фильтрацией. Рекурсивно обходит директории в поисках логов."""

    def __init__(self, config: LogViewerConfig):
        self.config = config
        if self.config.only_keys is None or not self.config.only_keys:
            self.config.only_keys = list(Filters().__dict__.values())

    def collect_logs(self) -> list[dict[str, Any]]:
        """Сбор всех логов за 1 проход"""
        logs = []

        for file in self.config.root_path.rglob('*'):  # noqa
            if any(excl in file.parts for excl in self.config.exclude_dirs):
                continue

            if file.parent.name == 'logs' and file.match(self.config.log_pattern):  # noqa
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                logs.append(json.loads(line))
                except (json.JSONDecodeError, OSError):
                    continue

        return logs

    def format_rows(self, logs: list[dict[str, Any]], keys: list[str]) -> list[str]:
        """Форматирование строк с выравниванием колонок"""
        if not logs:
            return []

        # 1. Собираем все значения и считаем максимальную длину для каждой колонки
        rows_data = []
        col_widths = [0] * len(keys)

        for log in logs:
            row_values = []
            for i, key in enumerate(keys):
                value = log.get(key, '')
                # Обрезаем длинные сообщения
                if key == 'message' and len(str(value)) > 80:
                    value = str(value)[:77] + '...'
                value = str(value)
                row_values.append(value)
                # Обновляем максимальную ширину колонки
                col_widths[i] = max(col_widths[i], len(value))
            rows_data.append(row_values)

        # 2. Форматируем строки с выравниванием
        separator = self.config.separator
        formatted_rows = []

        for row_values in rows_data:
            # Выравниваем каждое значение по ширине колонки
            aligned_values = []
            for i, value in enumerate(row_values):
                # Выравнивание по левому краю с отступом справа
                aligned_values.append(value.ljust(col_widths[i]))
            formatted_rows.append(separator.join(aligned_values))

        return formatted_rows

    def view(self) -> None:
        """Главный метод - сбор, сортировка и вывод"""
        trace_id = self.config.search_filters.trace_id
        request_id = self.config.search_filters.request_id
        component = self.config.search_filters.component

        search_parameters = 'Фильтры:'

        if trace_id is not None:
            search_parameters += f' trace_id : {trace_id} '

        if request_id is not None:
            search_parameters += f' request_id : {request_id} '

        if component is not None:
            search_parameters += f' component : {component} '

        logs = self.collect_logs()

        if not logs:
            print("❌ Логи не найдены")
            return

        if trace_id:
            logs = [log for log in logs if log.get(Filters.trace_id) == trace_id]

        if request_id:
            logs = [log for log in logs if log.get(Filters.request_id) == request_id]

        if component:
            logs = [log for log in logs if log.get(Filters.component) == component]

        if not logs:
            print(f"❌ Нет записей с trace_id: {trace_id}")
            return

        # Сортировка по дате
        logs.sort(key=lambda x: datetime.strptime(x['date'], self.config.date_format))

        # Форматирование с выравниванием
        keys = self.config.only_keys
        formatted_rows = self.format_rows(logs, keys)

        print("-" * 60)
        print(search_parameters)
        print("-" * 60)

        for row in formatted_rows:
            print(row)


# ============ Использование ============
if __name__ == '__main__':
    fltrs = Filters()
    search_fltrs = SearchFilters(
        # trace_id='8ac35890',
        # request_id=None,
        # component='audio_input',
    )

    config_log = LogViewerConfig(
        root_path=Path.cwd(),
        only_keys=[
            fltrs.component,
            fltrs.level,
            fltrs.event,
            fltrs.trace_id,
            fltrs.date,
            fltrs.request_id,
        ],
        separator='     ',
        search_filters=search_fltrs,
    )
    viewer = LogViewer(config_log)
    viewer.view()
