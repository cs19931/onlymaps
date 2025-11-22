# Copyright (c) 2025 Manos Stoumpos
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
This module contains fixtures relating to unique integer generation.
"""

from typing import Callable

import pytest


@pytest.fixture(scope="session")
def uid_factory() -> Callable[[], int]:
    """
    A unique integer factory function.
    """

    uid = 0

    def increment() -> int:
        nonlocal uid
        uid += 1
        return uid

    return increment


@pytest.fixture(scope="function")
def uid(uid_factory: Callable[[], int]) -> int:
    """
    Returns an integer that is unique among all tests.
    """
    return uid_factory()
