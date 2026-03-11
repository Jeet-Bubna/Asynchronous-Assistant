from threading import Thread
from typing import Callable, Iterable, Mapping, Any

import logging
logger = logging.getLogger(__name__)

class WorkerThread(Thread):
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = (), kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) :
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
    
    def update_args(self, new_args):
        self._args = (new_args, )

class Packets:
    def __init__(self, content:str, destination:Callable, priority:float) -> None:
        self._content = content
        self._destiation = destination
        self._priority = priority