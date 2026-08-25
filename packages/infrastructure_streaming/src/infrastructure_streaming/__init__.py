from infrastructure_streaming.consumer import consume_stream
from infrastructure_streaming.stream_v1 import StreamPipe, stream_pipeline

__all__ = [
    'consume_stream',  # streaming клиент
    'stream_pipeline', 'StreamPipe',  # универсальный stream конвейер
]
