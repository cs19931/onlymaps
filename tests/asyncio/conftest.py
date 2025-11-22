

import asyncio
import sys

# NOTE: Include this to overcome psycopg event loop policiy issue on Windows.
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from tests.asyncio.fixtures.connections import (  # type: ignore
    connection,
    connection_B,
    pool,
)
from tests.fixtures.executors import task_executor as executor
