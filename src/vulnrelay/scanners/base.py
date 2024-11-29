import abc
from typing import Any

_scanner_registry: dict[str, type["Scanner"]] = {}


class Scanner(abc.ABC):
    def __init_subclass__(cls, name: str, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        _scanner_registry[name] = cls

    @classmethod
    def has_scanner(cls, scanner_name: str) -> bool:
        return scanner_name in _scanner_registry

    @classmethod
    def get_scanner(cls, scanner_name: str) -> type["Scanner"]:
        return _scanner_registry[scanner_name]

    @classmethod
    def list_available(cls) -> list[str]:
        return list(_scanner_registry.keys())

    @abc.abstractmethod
    def defectdojo_name(self) -> str: ...

    @abc.abstractmethod
    def scan_image(self, image_name: str) -> str: ...

    @abc.abstractmethod
    def scan_host(self) -> str: ...
