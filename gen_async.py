# Copyright (c) 2025 Manos Stoumpos
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
This script is used to generate all `onlymaps.asyncio` modules.
"""

import re
from pathlib import Path

ASYNC_MARKER = "async"
AWAIT_MARKER = "await"
INCLUDE_MARKER = "include"
REPLACE_MARKER = "replace"
IGNORE_MARKER = "ignore"

# Tokens
PB_SPACE_OR_START = (
    r"(?:(?<=^)|(?<=\s)|(?<=`)|(?<=\")|(?<=\.)|(?<=\[)|(?<={)|(?<=_)|(?<=@)|(?<=\())"
)
DEF = "def"
FOR = "for"
WITH = "with"
ENTER = "__enter__"
EXIT = "__exit__"
CONTEXT_MANAGER = "contextmanager"
CONTEXT_MANAGER_TYPE = "ContextManager"
ITERATOR = "Iterator"
QUERY = "Query"
DATABASE = "Database"
CONNECTION = "Connection"
CONNECTION_POOL = "ConnectionPool"
SAFE_CURSOR = "SafeCursor"
PY_DB_CURSOR = "PyDbAPIv2Cursor"
PY_DB_CONNECTION = "PyDbAPIv2Connection"
PY_DB_MODULE = "PyDbAPIv2Module"
PY_DB_CONNECTION_FACTORY = "PyDbAPIv2ConnectionFactory"
PACKAGE = "onlymaps"
TESTS = "tests"
ASYNCIO = "asyncio"
FIXTURES = "fixtures"
INIT_MODULE = "__init__"
SPEC_MODULE = "_spec"
QUERY_MODULE = "_query"
CONNECTION_MODULE = "_connection"
POOL_MODULE = "_pool"
CONN_FACTORY_FUNCTION = "get_pydbapiv2_conn_factory_and_driver"
ASYNC_CONN_FACTORY_FUNCTION = "get_async_pydbapiv2_conn_factory_and_driver"
FIXTURE_CONNECTIONS_MODULE = "connections"
ONLYMAPS_SPEC = f"{PACKAGE}.{SPEC_MODULE}"
ONLYMAPS_QUERY = f"{PACKAGE}.{QUERY_MODULE}"
ONLYMAPS_CONNECTION = f"{PACKAGE}.{CONNECTION_MODULE}"
ONLYMAPS_POOL = f"{PACKAGE}.{POOL_MODULE}"
TESTS_FIXTURES_CONNECTION = f"{TESTS}.{FIXTURES}.{FIXTURE_CONNECTIONS_MODULE}"


# NOTE: Order matters.
ASYNC = [
    rf"{PB_SPACE_OR_START}{DEF}(?=\s)",
    rf"{PB_SPACE_OR_START}{FOR}(?=\s)",
    rf"{PB_SPACE_OR_START}{WITH}(?=\s)",
    rf"{PB_SPACE_OR_START}{ENTER}",
    rf"{PB_SPACE_OR_START}{EXIT}",
]
SPECIAL = [
    ONLYMAPS_CONNECTION,
    ONLYMAPS_SPEC,
    ONLYMAPS_QUERY,
    ONLYMAPS_POOL,
    CONTEXT_MANAGER,
    ITERATOR,
    QUERY,
    SAFE_CURSOR,
    DATABASE,
    CONTEXT_MANAGER_TYPE,
    PY_DB_CONNECTION_FACTORY,
    PY_DB_CONNECTION,
    PY_DB_MODULE,
    CONNECTION_POOL,
    CONNECTION,
    PY_DB_CURSOR,
    CONN_FACTORY_FUNCTION,
    TESTS_FIXTURES_CONNECTION,
]

RE_SPECIAL = re.compile(rf"(\sa\s)?(`)?{PB_SPACE_OR_START}({'|'.join(SPECIAL)})")

RE_ASYNC = re.compile(
    rf"(?:{'|'.join(ASYNC)})(?=.*# <{ASYNC_MARKER}(?:/{AWAIT_MARKER})?>)"
)
RE_AWAIT = re.compile(
    rf"(?<=\s)(?:[\w.]+)(?=\(.*# <(?:{ASYNC_MARKER}/)?{AWAIT_MARKER}>)"
)

_RE_COMMENTS = r"(?!.*>.*)(?:\s(.+))?"
RE_REPLACE = re.compile(rf"^(\s*).+?\s*#\s<{REPLACE_MARKER}:(.+)>{_RE_COMMENTS}$")
RE_INCLUDE = re.compile(
    rf"(?:{PB_SPACE_OR_START}#\s<{INCLUDE_MARKER}:)(.+)(?:>){_RE_COMMENTS}"
)
RE_IGNORE = re.compile(rf"{PB_SPACE_OR_START}#\s<{IGNORE_MARKER}>")


def sub_special(m: re.Match) -> str:

    ms = m.group(3)

    if ms == CONTEXT_MANAGER:
        return "asynccontextmanager"
    if ms == ONLYMAPS_SPEC:
        return f"{PACKAGE}.{ASYNCIO}.{SPEC_MODULE}"
    if ms == ONLYMAPS_QUERY:
        return f"{PACKAGE}.{ASYNCIO}.{QUERY_MODULE}"
    if ms == ONLYMAPS_CONNECTION:
        return f"{PACKAGE}.{ASYNCIO}.{CONNECTION_MODULE}"
    if ms == ONLYMAPS_POOL:
        return f"{PACKAGE}.{ASYNCIO}.{POOL_MODULE}"
    if ms == CONN_FACTORY_FUNCTION:
        return ASYNC_CONN_FACTORY_FUNCTION
    if ms == TESTS_FIXTURES_CONNECTION:
        return f"{TESTS}.{ASYNCIO}.{FIXTURES}.{FIXTURE_CONNECTIONS_MODULE}"
    if ms in {
        ITERATOR,
        QUERY,
        SAFE_CURSOR,
        DATABASE,
        CONTEXT_MANAGER_TYPE,
        CONNECTION,
        CONNECTION_POOL,
        PY_DB_MODULE,
        PY_DB_CURSOR,
        PY_DB_CONNECTION,
        PY_DB_CONNECTION_FACTORY,
    }:
        article = " an " if m.group(1) else ""
        backtick = btck if (btck := m.group(2)) else ""
        return f"{article}{backtick}Async{ms}"

    raise ValueError(f"Invalid token: `{ms}`")


def sub_async(m: re.Match) -> str:

    ms = m.group(0)

    if ms in {DEF, FOR, WITH}:
        return f"async {ms}"
    if ms == ENTER:
        return "__aenter__"
    if ms == EXIT:
        return "__aexit__"

    raise ValueError(f"Invalid token: `{ms}`")


def sub_await(m: re.Match) -> str:
    return f"await {m.group(0)}"


def sub_include(m: re.Match) -> str:
    line = m.group(1)
    line += f" # <{INCLUDE_MARKER}>"
    if extra_comments := m.group(2):
        line += f" {extra_comments}"
    return line


def sub_replace(m: re.Match) -> str:
    line = m.group(1) + m.group(2)
    line += f" # <{REPLACE_MARKER}>"
    if extra_comments := m.group(3):
        line += f" {extra_comments}"
    return line


def main():

    file_paths = [
        f"./{PACKAGE}/{INIT_MODULE}.py",
        f"./{PACKAGE}/{INIT_MODULE}.pyi",
        f"./{PACKAGE}/{SPEC_MODULE}.py",
        f"./{PACKAGE}/{CONNECTION_MODULE}.py",
        f"./{PACKAGE}/{POOL_MODULE}.py",
        f"./{PACKAGE}/{QUERY_MODULE}.py",
        f"./{TESTS}/{FIXTURES}/{FIXTURE_CONNECTIONS_MODULE}.py",
        f"./{TESTS}/test_connect.py",
        f"./{TESTS}/test_database.py",
        f"./{TESTS}/test_connection.py",
        f"./{TESTS}/test_pool.py",
        f"./{TESTS}/test_query.py",
    ]

    Path(f"./{PACKAGE}/{ASYNCIO}").mkdir(exist_ok=True)
    Path(f"./{TESTS}/{ASYNCIO}/{FIXTURES}").mkdir(exist_ok=True)

    for fp in file_paths:

        path = Path(fp)

        async_file = ""
        ignore = False

        with open(path, "r") as file:
            for line in file.readlines():
                if RE_IGNORE.search(line):
                    ignore = not ignore
                if not ignore:
                    line = RE_INCLUDE.sub(sub_include, line)
                    line = RE_REPLACE.sub(sub_replace, line)
                    line = RE_SPECIAL.sub(sub_special, line)
                    line = RE_ASYNC.sub(sub_async, line)
                    line = RE_AWAIT.sub(sub_await, line)
                    async_file += line

        if len(path.parts) == 2:
            asyncio_path = f"./{path.parent}/{ASYNCIO}/{path.name}"
        elif len(path.parts) == 3:
            parent = path.parent
            asyncio_path = f"./{parent.parent}/{ASYNCIO}/{parent.name}/{path.name}"
        else:
            raise ValueError(f"Invalid path: `{path}`.")

        with open(asyncio_path, "w+", encoding="utf-8") as f:
            f.write(async_file)


if __name__ == "__main__":
    main()
