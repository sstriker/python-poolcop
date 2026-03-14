Asynchronous Python client for the [PoolCopilot API][poolcopilot-api].

## About

A python package to interact with a [PoolCop][poolcop] device through the PoolCopilot API.

## Installation

```bash
pip install poolcop
```

## Usage

```python
import asyncio
import json
from poolcop import PoolCopilot

API_KEY="xxxxxxxxxxxxxxxxxxxxxxx"

async def main() -> None:
    """Show example on fetching the status from PoolCop."""
    async with PoolCopilot(api_key=API_KEY) as client:
        status = await client.status()
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
```

## API Features

The PoolCopilot API provides access to various features of your PoolCop device:

### Status Information
- Water and air temperature
- pH and ORP (Oxidation-Reduction Potential) values
- Water level status
- Valve position
- Pump status and speed
- Equipment status (auxiliaries, etc.)
- Filter settings and timers
- Forced filtration status and remaining time

### Commands
- Toggle pump on/off
- Set pump speed (for multi-speed pumps)
- Toggle auxiliary outputs
- Set valve position
- Clear alarms
- Set forced filtration mode (24h, 48h, or 72h)

### History
- Alarm history (with pagination)
- Command history (with pagination)

### Quota Management
- `token_limit` — remaining API calls in the current window
- `token_expire` — epoch timestamp when the current quota window resets

### Options
- `lang` parameter — sets the `X-PoolCopilot-Lang` header for localised responses

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
git clone https://github.com/sstriker/python-poolcop.git
cd python-poolcop
poetry install --with dev
poetry run pytest
```

### Releasing to PyPI

The repository uses [trusted publishing](https://docs.pypi.org/trusted-publishers/) via GitHub Actions. To release:

1. Bump the version in `pyproject.toml`
2. Merge to `main`
3. Create a GitHub Release (this creates a tag and triggers the publish workflow)
4. The workflow runs tests, builds with Poetry, and publishes to PyPI automatically

[poolcop]: https://www.poolcop.com/
[poolcopilot-api]: https://poolcopilot.com/api/docs/
