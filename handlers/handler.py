from __future__ import annotations
from abc import ABC, abstractmethod


class TimeHandler:
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, **request):
        pass
