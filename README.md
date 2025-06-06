Getting started
---------------

- Change directory into your newly created project.

    ``cd Iot_events_monitoring``


- Install build dependencies.

    ``sudo apt-get install clang libpq-dev``


- Install uv project manager.


    *On macOS or Linux*

    ``curl -LsSf https://astral.sh/uv/install.sh | sh``


    *On Windows*

    ``powershell -c "irm https://astral.sh/uv/install.ps1 | iex"``


- Install the project

    ``uv python pin 3.12.1``

    ``uv venv``

    ``uv sync``

    ``source .venv/bin/activate``


- Format code commands

    ``ruff check --unsafe-fixes --fix``

    ``ruff format``
