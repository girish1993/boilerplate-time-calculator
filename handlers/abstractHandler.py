from __future__ import annotations
from handler import TimeHandler
from abc import ABC, abstractmethod


class AbstractTimeHandler(TimeHandler):
    _next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, **request):
        if self._next_handler:
            return self._next_handler.handle(**request)
        return None
