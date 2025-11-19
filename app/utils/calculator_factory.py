"""Lightweight calculator factory with lazy caching."""
from functools import lru_cache
from typing import Type, TypeVar

T = TypeVar("T")


@lru_cache(maxsize=None)
def get_calculator(calculator_cls: Type[T]) -> T:
    """Return a cached calculator instance, creating it on first use."""
    return calculator_cls()

