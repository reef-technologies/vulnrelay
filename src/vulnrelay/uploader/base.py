import abc


class Uploader(abc.ABC):
    @abc.abstractmethod
    def upload_scan_result(self, *, service: str, scan_type: str, content: str) -> None:
        pass
