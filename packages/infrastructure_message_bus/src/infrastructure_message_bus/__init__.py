from infrastructure_message_bus.main import MessagePrintSettings, FileLogSettings
from infrastructure_message_bus.factory import message_bus_factory

temp_variable = 1000

__all__ = [
    'temp_variable',
    'MessagePrintSettings', 'FileLogSettings',  # типы настроек
    'message_bus_factory',  # фабрика
]
