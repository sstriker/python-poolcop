"""Asynchronous client for the PoolCopilot API."""
from __future__ import annotations

import asyncio
import socket
import time
from dataclasses import dataclass
from typing import Any, cast

import async_timeout
from http import HTTPStatus
from aiohttp.client import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET, METH_POST
from yarl import URL

from .const import API_HOST, USER_AGENT
from .exceptions import (
    PoolCopilotConnectionError,
    PoolCopilotInvalidKeyError,
    PoolCopilotRateLimitError,
    PoolCopilotError,
)


@dataclass
class PoolCopilot:
    """Main class for handling data fetching from PoolCopilot."""

    api_key: str | None = None
    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False
    _token: str = None
    _token_expire: int = 0
    _token_limit: int | None = None
    _poolcop_id: int | None = None

    @property
    def poolcop_id(self):
        """Primary PoolCop Identifier"""
        return self._poolcop_id

    def _build_url(self, uri):
        return URL.build(scheme="https", host=API_HOST, path=f"/api/v1/{uri}")

    def _headers(self):
        headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if self._token is not None:
            headers["PoolCop-Token"] = self._token
        return headers

    async def _authenticate(self) -> None:
        """Authenticate and store a token"""

        expire_in = self._token_expire - time.time()
        if self._token is not None and expire_in > 0:
            # Valid token
            return

        self._token = None
        self._token_limit = None
        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.post(
                    self._build_url("token"),
                    data={"APIKEY": self.api_key},
                    headers=self._headers(),
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise PoolCopilotConnectionError(
                "Timeout occurred while connecting to the API."
            ) from exception
        except ClientResponseError as exception:
            if exception.code == HTTPStatus.FORBIDDEN:
                raise PoolCopilotInvalidKeyError(
                    "Could not authenticate with the provided API key."
                ) from exception
            raise PoolCopilotConnectionError(
                "Error occurred while communicating with the API."
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            raise PoolCopilotConnectionError(
                "Error occurred while communicating with the API."
            ) from exception

        data = await response.json()

        self._token = data.get("token", None)
        if self._token is None:
            raise PoolCopilotInvalidKeyError(
                "Could not authenticate with the provided API key."
            )
        # self._parse_token(data.get("values", {"max_limit": 1}))

    def _parse_token(self, api_token):
        self._token_limit = int(api_token.get("max_limit", 0))
        self._token_expire = int(api_token.get("expire", 0))
        self._poolcop_id = api_token.get("poolcop_id", self._poolcop_id)

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the API of PoolCopilot.

        Args:
        ----
            uri: Request URI, without leading '/', e.g. 'status'
            method: HTTP method to use, e.g. 'GET'

        Returns:
        -------
            A Python dictionary (json) with the response from PoolCopilot.

        Raises:
        ------
            PoolCopilotConnectionError: An error occurred while
                communicating with the API.
            PoolCopilotRateLimitError: The request limit for
                the API token was exceeded.
            PoolCopilotError: Received an unexpected response from
                the API.
        """

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        await self._authenticate()

        if self._token_limit == 0:
            raise PoolCopilotRateLimitError("Rate limit hit")

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    self._build_url(uri),
                    headers=self._headers(),
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the API."
            raise PoolCopilotConnectionError(
                msg,
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with the API."
            raise PoolCopilotConnectionError(
                msg,
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the PoolCopilot API"
            raise PoolCopilotError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        data = cast(dict[str, Any], await response.json())
        self._parse_token(data.get("api_token", {}))
        return data

    async def status(self) -> dict[str, Any]:
        """Get PoolCop status."""
        data = await self._request(
            "status",
        )
        return data

    async def alarm_history(self, offset: int = 0) -> dict[str, Any]:
        """Get PoolCop alarm history."""
        data = await self._request(
            f"history/alarms/{offset}",
        )
        return data

    async def command_history(self, offset: int = 0) -> dict[str, Any]:
        """Get PoolCop command history."""
        return await self._request(f"history/commands/{offset}")

    async def toggle_pump(self) -> dict[str, Any]:
        """Toggle pump on/off."""
        return await self._request("command/pump", method=METH_POST)

    async def set_pump_speed(self, speed: int) -> dict[str, Any]:
        """Set pump to a certain speed."""
        assert speed in {1, 2, 3}
        return await self._request(f"command/pump/{speed}", method=METH_POST)

    async def toggle_aux(self, aux_id: int) -> dict[str, Any]:
        """Toggle aux on/off."""
        return await self._request("command/aux/{aux_id}", method=METH_POST)

    async def clear_alarm(self) -> dict[str, Any]:
        """Clear alarm."""
        return await self._request("command/clear_alarm", method=METH_POST)

    async def set_valve_position(self, position: int) -> dict[str, Any]:
        """Set valve in a certain position."""
        return await self._request("command/valve/{position}", method=METH_POST)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()
            self.session = None

    async def __aenter__(self) -> PoolCopilot:
        """Async enter.

        Returns
        -------
            The PoolCopilot object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
