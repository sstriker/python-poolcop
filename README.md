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
- Alarm history
- Command history

## Development

This project includes a development container configuration for Visual Studio Code, which provides an isolated, reproducible development environment.

### Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/)
- [VS Code Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/sstriker/python-poolcop.git
   cd python-poolcop
   ```

2. Open the project in VS Code:
   ```bash
   code .
   ```

3. When prompted "Reopen in Container", click it, or run the "Remote-Containers: Reopen in Container" command from the Command Palette (F1).

4. VS Code will build the development container and install all dependencies automatically.

5. Start developing! Your changes will be isolated to the container environment.

[poolcop]: https://www.poolcop.com/
[poolcopilot-api]: https://poolcopilot.com/api/docs/
