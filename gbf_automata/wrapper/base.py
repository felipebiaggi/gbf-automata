from __future__ import annotations
from typing import Any, Tuple
from abc import ABCMeta, abstractmethod


class PointerBase(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    def __enter__(self) -> PointerBase:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()
        pass

    @abstractmethod
    def close(self) -> None:
        """Clean-up"""
        pass

    @abstractmethod
    def get_position(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def set_position(self, x: int, y: int) -> None:
        pass
