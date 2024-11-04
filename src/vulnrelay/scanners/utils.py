from .base import Scanner


def validate_scanner(name: str) -> str:
    if not Scanner.has_scanner(name):
        raise ValueError(f"Invalid scanner: {name}. Available scanners: {Scanner.list_available()}")
    return name
