from infrastructure_message_bus.main import MessagePrintSettings, FileLogSettings
from infrastructure_message_bus.factory import message_bus_factory

temp_var = 100

__all__ = [
    'temp_var',
    'MessagePrintSettings', 'FileLogSettings',  # типы настроек
    'message_bus_factory',  # фабрика
]
