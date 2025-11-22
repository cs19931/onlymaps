# Copyright (c) 2025 Manos Stoumpos
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
This module contains tests related to various utility functions.
"""

import pytest

from onlymaps._drivers import Driver
from onlymaps._utils import ConnInfo, decompose_conn_str, try_import_module


@pytest.mark.parametrize(
    "conn_str, conn_info",
    [
        (
            f"{Driver.POSTGRES}://www:password@host:5432/db",
            (Driver.POSTGRES, "host", 5432, "db", "www", "password"),
        ),
        (
            f"{Driver.MY_SQL}://www:password@host:5432/db",
            (Driver.MY_SQL, "host", 5432, "db", "www", "password"),
        ),
        (
            f"{Driver.SQL_SERVER}://www:password@host:5432/db",
            (Driver.SQL_SERVER, "host", 5432, "db", "www", "password"),
        ),
        (
            f"{Driver.MARIA_DB}://www:password@host:5432/db",
            (Driver.MARIA_DB, "host", 5432, "db", "www", "password"),
        ),
        (f"{Driver.SQL_LITE}:///db", (Driver.SQL_LITE, "", 0, "db", "", "")),
        (
            f"{Driver.POSTGRES}://www@host:5432/db",
            (Driver.POSTGRES, "host", 5432, "db", "www", None),
        ),
    ],
)
def test_decompose_conn_str(conn_str: str, conn_info: ConnInfo) -> None:
    """
    Tests successful decomposing of a connection string.
    """
    assert decompose_conn_str(conn_str) == conn_info


@pytest.mark.parametrize(
    "conn_str",
    [
        "random-string",
        "fakeprotocol://www:password@host:5432/db",
        f"{Driver.POSTGRES}/www:password@host:5432/db",
        f"{Driver.POSTGRES}://www:password|host:5432/db",
        f"{Driver.POSTGRES}://www:password@host/5432/db",
        f"{Driver.POSTGRES}://www:password@host:port/db",
        f"{Driver.POSTGRES}://www:password@host:5432/",
    ],
)
def test_decompose_conn_str_on_invalid_conn_str(conn_str: str) -> None:
    """
    Tests unsuccessful decomposing of a connection string.
    """
    with pytest.raises(ValueError):
        decompose_conn_str(conn_str)


def test_try_import_module() -> None:
    """
    Tests successful import of a module.
    """
    module_name = "pytest"
    module = try_import_module(module_name)
    assert getattr(module, "__name__") == module_name


def test_try_import_module_on_import_error() -> None:
    """
    Tests unsuccessful import of a module.
    """
    with pytest.raises(ImportError):
        try_import_module("unknown_module")
