"""Constants for PoolCopilot API client."""
from importlib import metadata
from typing import Final

API_HOST: Final = "poolcopilot.com"
USER_AGENT: Final = f"python-poolcop/{metadata.version(__package__)}"
