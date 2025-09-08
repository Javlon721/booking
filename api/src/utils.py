import copy
import time
from contextlib import contextmanager
from typing import Any, Callable

from pydantic import model_validator


def list_dict_keys(obj: dict) -> list[Any]:
    return list(obj.keys())


def deep_copy(obj: Any) -> Any:
    return copy.deepcopy(obj)


class SetNonesMixin:
    @model_validator(mode='before')
    @classmethod
    def check_card_number_not_present(cls, data: dict[str, Any]) -> Any:
        for field in cls.model_fields.keys():
            if field not in data:
                data.update({field: None})
        return data


@contextmanager
def performance_time(callback: Callable[[float], Any]):
    start = time.perf_counter()
    yield
    ended_in = time.perf_counter() - start
    callback(ended_in)
