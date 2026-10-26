class DownloadErr:
    class StatusError(RuntimeError):
        pass

    class Break(RuntimeError):
        pass

    class TimeoutError(RuntimeError):
        pass

    class Sha256MismatchPrimary(RuntimeError):
        pass

    class Sha256MismatchSecondary(RuntimeError):
        pass
