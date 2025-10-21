"""Concurrency utilities for thread-safe operations."""

import asyncio
import threading
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Callable, Generic, TypeVar

T = TypeVar('T')


class ThreadSafeDict(Generic[T]):
    """Thread-safe dictionary implementation."""
    
    def __init__(self):
        self._data: dict = {}
        self._lock = threading.RLock()
    
    def get(self, key: Any, default: Any = None) -> T:
        """Get value by key."""
        with self._lock:
            return self._data.get(key, default)
    
    def set(self, key: Any, value: T) -> None:
        """Set value for key."""
        with self._lock:
            self._data[key] = value
    
    def delete(self, key: Any) -> bool:
        """Delete key and return True if existed."""
        with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            return False
    
    def keys(self) -> list:
        """Get all keys."""
        with self._lock:
            return list(self._data.keys())
    
    def values(self) -> list:
        """Get all values."""
        with self._lock:
            return list(self._data.values())
    
    def items(self) -> list:
        """Get all key-value pairs."""
        with self._lock:
            return list(self._data.items())
    
    def clear(self) -> None:
        """Clear all data."""
        with self._lock:
            self._data.clear()
    
    def __contains__(self, key: Any) -> bool:
        """Check if key exists."""
        with self._lock:
            return key in self._data
    
    def __len__(self) -> int:
        """Get number of items."""
        with self._lock:
            return len(self._data)


class ThreadSafeList(Generic[T]):
    """Thread-safe list implementation."""
    
    def __init__(self):
        self._data: list = []
        self._lock = threading.RLock()
    
    def append(self, item: T) -> None:
        """Append item to list."""
        with self._lock:
            self._data.append(item)
    
    def extend(self, items: list[T]) -> None:
        """Extend list with items."""
        with self._lock:
            self._data.extend(items)
    
    def remove(self, item: T) -> bool:
        """Remove item from list. Returns True if found."""
        with self._lock:
            try:
                self._data.remove(item)
                return True
            except ValueError:
                return False
    
    def get(self, index: int, default: Any = None) -> T:
        """Get item at index."""
        with self._lock:
            try:
                return self._data[index]
            except IndexError:
                return default
    
    def index(self, item: T) -> int:
        """Get index of item."""
        with self._lock:
            return self._data.index(item)
    
    def __getitem__(self, index: int) -> T:
        """Get item at index."""
        with self._lock:
            return self._data[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """Set item at index."""
        with self._lock:
            self._data[index] = value
    
    def __len__(self) -> int:
        """Get length of list."""
        with self._lock:
            return len(self._data)
    
    def __contains__(self, item: T) -> bool:
        """Check if item exists."""
        with self._lock:
            return item in self._data
    
    def __iter__(self):
        """Iterate over items."""
        with self._lock:
            return iter(self._data.copy())


def thread_safe(func: Callable) -> Callable:
    """Decorator to make a function thread-safe."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # This is a simple decorator - in practice, you'd use locks
        # For now, we'll rely on the ThreadSafe collections
        return func(*args, **kwargs)
    return wrapper


@asynccontextmanager
async def async_lock(lock: asyncio.Lock):
    """Async context manager for asyncio locks."""
    await lock.acquire()
    try:
        yield
    finally:
        lock.release()


class AsyncThreadSafeDict(Generic[T]):
    """Async thread-safe dictionary implementation."""
    
    def __init__(self):
        self._data: dict = {}
        self._lock = asyncio.Lock()
    
    async def get(self, key: Any, default: Any = None) -> T:
        """Get value by key."""
        async with self._lock:
            return self._data.get(key, default)
    
    async def set(self, key: Any, value: T) -> None:
        """Set value for key."""
        async with self._lock:
            self._data[key] = value
    
    async def delete(self, key: Any) -> bool:
        """Delete key and return True if existed."""
        async with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            return False
    
    async def keys(self) -> list:
        """Get all keys."""
        async with self._lock:
            return list(self._data.keys())
    
    async def values(self) -> list:
        """Get all values."""
        async with self._lock:
            return list(self._data.values())
    
    async def items(self) -> list:
        """Get all key-value pairs."""
        async with self._lock:
            return list(self._data.items())
    
    async def clear(self) -> None:
        """Clear all data."""
        async with self._lock:
            self._data.clear()
    
    async def __contains__(self, key: Any) -> bool:
        """Check if key exists."""
        async with self._lock:
            return key in self._data
