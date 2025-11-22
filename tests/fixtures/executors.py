from asyncio import Task, create_task
from threading import Thread
from typing import Any, AsyncIterator, Awaitable, Callable, Iterator, Protocol

import pytest


class Executor(Protocol):

    def submit(self, fn: Callable, /, *args: Any, **kwargs: Any) -> None:
        """
        Submits a function for execution:

        :param Callable fn: The function to be executed.
        :param Any *args: Any positional arguments.
        :param Any **kwargs: Any keyword arguments.
        """

    def wait(self) -> Awaitable[None]:
        """
        Wait for all submitted tasks to finish execution.
        """


class ThreadExecutor:

    def __init__(self) -> None:
        """
        The `ThreadExecutor` constructor.
        """
        self.__threads: list[Thread] = []

    def submit(self, fn: Callable, /, *args: Any, **kwargs: Any) -> None:
        """
        Submits a function for execution.

        :param Callable fn: The function to be executed.
        :param Any *args: Any positional arguments.
        :param Any **kwargs: Any keyword arguments.
        """
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        self.__threads.append(thread)

    def wait(self) -> None:
        """
        Waits for all submitted functions to finish execution.
        """
        for thread in self.__threads:
            thread.join()


class TaskExecutor:

    def __init__(self) -> None:
        """
        The `TaskExecutor` constructor.
        """
        self.__tasks: list[Task] = []

    def submit(self, fn: Callable, *args: Any, **kwargs: Any) -> None:
        """
        Submits a coroutine for execution.

        :param Callable fn: The coroutine to be executed.
        :param Any *args: Any positional arguments.
        :param Any **kwargs: Any keyword arguments.
        """
        task = create_task(fn(*args, **kwargs))
        self.__tasks.append(task)

    async def wait(self) -> None:
        """
        Waits for all submitted coroutine to finish execution.
        """
        for task in self.__tasks:
            try:
                await task
            except:
                pass


@pytest.fixture(scope="function")
def thread_executor() -> Iterator[ThreadExecutor]:
    """
    Returns a thread executor.
    """
    executor = ThreadExecutor()
    yield executor
    executor.wait()


@pytest.fixture(scope="function")
async def task_executor() -> AsyncIterator[TaskExecutor]:
    """
    Returns a task executor.
    """
    executor = TaskExecutor()
    yield executor
    await executor.wait()
