"""Exceptions for PoolCopilot API client."""


class PoolCopilotError(Exception):
    """Generic PoolCopilot exception."""


class PoolCopilotConnectionError(PoolCopilotError):
    """PoolCopilot - Connection error."""


class PoolCopilotInvalidKeyError(PoolCopilotError):
    """PoolCopilot - API Key invalid."""


class PoolCopilotRateLimitError(PoolCopilotError):
    """PoolCopilot - Rate limit reached."""
