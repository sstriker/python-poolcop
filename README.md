Asynchronous Python client for the [PoolCopilot API][poolcopilot-api].

## About

A python package to interact with a [PoolCop][poolcop] device.

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

[poolcop]: https://www.poolcop.com/
[poolcopilot-api]: https://poolcopilot.com/api/docs/
