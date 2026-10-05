class DownloadErr:
    class StatusError(RuntimeError):
        pass

    class Break(RuntimeError):
        pass

    class TimeoutError(RuntimeError):
        pass
