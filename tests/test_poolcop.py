"""Tests for the PoolCopilot API client."""

import pytest
from aiohttp import ClientSession
from aioresponses import aioresponses

from poolcop import (
    PoolCopilot,
    PoolCopilotConnectionError,
    PoolCopilotInvalidKeyError,
    PoolCopilotRateLimitError,
)

TOKEN_URL = "https://poolcopilot.com/api/v1/token"
STATUS_URL = "https://poolcopilot.com/api/v1/status"
BASE_URL = "https://poolcopilot.com/api/v1"

TOKEN_RESPONSE = {
    "token": "test-token-123",
    "values": {"max_limit": 90, "expire": 9999999999},
}

STATUS_RESPONSE = {
    "api_token": {"max_limit": 89, "expire": 9999999999, "poolcop_id": 42},
    "PoolCop": {
        "status": {"pump": 1, "poolcop": 3},
        "temperature": {"water": 26.5},
    },
}


@pytest.fixture
def poolcop():
    """Create a PoolCopilot client."""
    return PoolCopilot(api_key="test-key")


@pytest.fixture
def mock_api():
    """Provide aioresponses mock."""
    with aioresponses() as m:
        yield m


def _mock_auth(mock_api, repeat=False):
    """Add auth token response to mock."""
    mock_api.post(TOKEN_URL, payload=TOKEN_RESPONSE, repeat=repeat)


async def test_status(poolcop, mock_api):
    """Test fetching status."""
    _mock_auth(mock_api)
    mock_api.get(STATUS_URL, payload=STATUS_RESPONSE)

    async with poolcop:
        data = await poolcop.status()

    assert data["PoolCop"]["temperature"]["water"] == 26.5
    assert poolcop.poolcop_id == 42


async def test_authentication_failure(poolcop, mock_api):
    """Test that invalid API key raises PoolCopilotInvalidKeyError."""
    mock_api.post(TOKEN_URL, status=403)

    async with poolcop:
        with pytest.raises(PoolCopilotInvalidKeyError):
            await poolcop.status()


async def test_authentication_no_token(poolcop, mock_api):
    """Test that missing token in response raises PoolCopilotInvalidKeyError."""
    mock_api.post(TOKEN_URL, payload={"no_token": True})

    async with poolcop:
        with pytest.raises(PoolCopilotInvalidKeyError):
            await poolcop.status()


async def test_connection_error(poolcop, mock_api):
    """Test connection error handling."""
    from aiohttp import ClientError

    mock_api.post(TOKEN_URL, exception=ClientError("conn refused"))

    async with poolcop:
        with pytest.raises(PoolCopilotConnectionError):
            await poolcop.status()


async def test_rate_limit(poolcop, mock_api):
    """Test rate limit detection."""
    _mock_auth(mock_api)
    # Simulate rate limit by setting _token_limit to 0
    poolcop._token = "some-token"
    poolcop._token_expire = 9999999999
    poolcop._token_limit = 0

    async with poolcop:
        with pytest.raises(PoolCopilotRateLimitError):
            await poolcop.status()


async def test_toggle_pump(poolcop, mock_api):
    """Test toggle pump command."""
    _mock_auth(mock_api)
    mock_api.post(
        f"{BASE_URL}/command/pump",
        payload={"api_token": {"max_limit": 88}, "result": "ok"},
    )

    async with poolcop:
        result = await poolcop.toggle_pump()
    assert result["result"] == "ok"


async def test_set_pump_speed_valid(poolcop, mock_api):
    """Test setting valid pump speeds."""
    _mock_auth(mock_api, repeat=True)
    for speed in (1, 2, 3):
        mock_api.post(
            f"{BASE_URL}/command/pump/{speed}",
            payload={"api_token": {"max_limit": 87}, "result": "ok"},
        )

    async with poolcop:
        for speed in (1, 2, 3):
            result = await poolcop.set_pump_speed(speed)
            assert result["result"] == "ok"


async def test_set_pump_speed_invalid(poolcop):
    """Test that invalid pump speed raises ValueError."""
    with pytest.raises(ValueError, match="Invalid pump speed"):
        await poolcop.set_pump_speed(5)

    with pytest.raises(ValueError, match="Invalid pump speed"):
        await poolcop.set_pump_speed(0)


async def test_toggle_aux(poolcop, mock_api):
    """Test toggle aux command uses f-string correctly."""
    _mock_auth(mock_api)
    mock_api.post(
        f"{BASE_URL}/command/aux/4",
        payload={"api_token": {"max_limit": 86}, "result": "ok"},
    )

    async with poolcop:
        result = await poolcop.toggle_aux(4)
    assert result["result"] == "ok"


async def test_toggle_auxiliary_alias(poolcop, mock_api):
    """Test that toggle_auxiliary is an alias for toggle_aux."""
    _mock_auth(mock_api)
    mock_api.post(
        f"{BASE_URL}/command/aux/4",
        payload={"api_token": {"max_limit": 85}, "result": "ok"},
    )

    async with poolcop:
        result = await poolcop.toggle_auxiliary(4)
    assert result["result"] == "ok"


async def test_set_valve_position(poolcop, mock_api):
    """Test set valve position uses f-string correctly."""
    _mock_auth(mock_api)
    mock_api.post(
        f"{BASE_URL}/command/valve/3",
        payload={"api_token": {"max_limit": 84}, "result": "ok"},
    )

    async with poolcop:
        result = await poolcop.set_valve_position(3)
    assert result["result"] == "ok"


async def test_set_force_filtration_valid(poolcop, mock_api):
    """Test valid forced filtration durations."""
    _mock_auth(mock_api, repeat=True)
    for hours in (24, 48, 72):
        mock_api.post(
            f"{BASE_URL}/command/force/{hours}",
            payload={"api_token": {"max_limit": 83}, "result": "ok"},
        )

    async with poolcop:
        for hours in (24, 48, 72):
            result = await poolcop.set_force_filtration(hours)
            assert result["result"] == "ok"


async def test_set_force_filtration_invalid(poolcop):
    """Test that invalid filtration hours raises ValueError."""
    with pytest.raises(ValueError, match="Invalid forced filtration"):
        await poolcop.set_force_filtration(12)


async def test_no_lang_header_by_default(poolcop):
    """Test that X-PoolCopilot-Lang header is not sent by default."""
    headers = poolcop._headers()
    assert "X-PoolCopilot-Lang" not in headers


async def test_lang_header_when_set():
    """Test that X-PoolCopilot-Lang header is sent when lang is set."""
    poolcop = PoolCopilot(api_key="test-key", lang="en")
    headers = poolcop._headers()
    assert headers["X-PoolCopilot-Lang"] == "en"


async def test_lang_header_custom_value():
    """Test that lang header uses the configured language."""
    poolcop = PoolCopilot(api_key="test-key", lang="fr")
    headers = poolcop._headers()
    assert headers["X-PoolCopilot-Lang"] == "fr"


async def test_alarm_history(poolcop, mock_api):
    """Test alarm history endpoint."""
    _mock_auth(mock_api)
    mock_api.get(
        f"{BASE_URL}/history/alarms/0",
        payload={"api_token": {"max_limit": 82}, "alarms": []},
    )

    async with poolcop:
        result = await poolcop.alarm_history(0)
    assert result["alarms"] == []


async def test_clear_alarm(poolcop, mock_api):
    """Test clear alarm command."""
    _mock_auth(mock_api)
    mock_api.post(
        f"{BASE_URL}/command/clear_alarm",
        payload={"api_token": {"max_limit": 81}, "result": "ok"},
    )

    async with poolcop:
        result = await poolcop.clear_alarm()
    assert result["result"] == "ok"


async def test_close_session(mock_api):
    """Test that close() closes a self-created session."""
    poolcop = PoolCopilot(api_key="test-key")
    _mock_auth(mock_api)
    mock_api.get(STATUS_URL, payload=STATUS_RESPONSE)

    # This should create and then close its own session
    async with poolcop:
        await poolcop.status()

    assert poolcop.session is None


async def test_token_limit_none_before_any_call(poolcop):
    """Test that token_limit is None before any API call."""
    assert poolcop.token_limit is None


async def test_token_limit_after_status(poolcop, mock_api):
    """Test that token_limit reflects API response after status call."""
    _mock_auth(mock_api)
    mock_api.get(STATUS_URL, payload=STATUS_RESPONSE)

    async with poolcop:
        await poolcop.status()

    assert poolcop.token_limit == 89


async def test_token_expire_default(poolcop):
    """Test that token_expire is 0 before any call."""
    assert poolcop.token_expire == 0


async def test_token_expire_after_status(poolcop, mock_api):
    """Test that token_expire reflects API response after status call."""
    _mock_auth(mock_api)
    mock_api.get(STATUS_URL, payload=STATUS_RESPONSE)

    async with poolcop:
        await poolcop.status()

    assert poolcop.token_expire == 9999999999


async def test_provided_session_not_closed(mock_api):
    """Test that a user-provided session is not closed."""
    session = ClientSession()
    poolcop = PoolCopilot(api_key="test-key", session=session)
    _mock_auth(mock_api)
    mock_api.get(STATUS_URL, payload=STATUS_RESPONSE)

    async with poolcop:
        await poolcop.status()

    # Session should still be open
    assert not session.closed
    await session.close()


async def test_request_non_json_content_type(poolcop, mock_api):
    """text/html → PoolCopilotError."""
    from poolcop import PoolCopilotError

    _mock_auth(mock_api)
    mock_api.get(
        STATUS_URL,
        body="<html>Error</html>",
        content_type="text/html",
    )

    async with poolcop:
        with pytest.raises(PoolCopilotError):
            await poolcop.status()


async def test_request_connection_error(poolcop, mock_api):
    """socket.gaierror during request."""
    import socket

    _mock_auth(mock_api)
    mock_api.get(STATUS_URL, exception=socket.gaierror("DNS failure"))

    async with poolcop:
        with pytest.raises(PoolCopilotConnectionError):
            await poolcop.status()


async def test_command_history(poolcop, mock_api):
    """Correct endpoint called."""
    _mock_auth(mock_api)
    mock_api.get(
        f"{BASE_URL}/history/commands/0",
        payload={"api_token": {"max_limit": 80}, "commands": []},
    )

    async with poolcop:
        result = await poolcop.command_history(0)
    assert result["commands"] == []
