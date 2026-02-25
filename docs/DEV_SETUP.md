# DEV_SETUP

## Linux
1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -e .[dev]`
4. `is_auto smoke --out runs`
5. `pytest -q`
6. `ruff check src tests tools`

## Windows (PowerShell)
1. `python -m venv .venv`
2. `.venv\Scripts\Activate.ps1`
3. `pip install -e .[dev]`
4. `is_auto smoke --out runs`
5. `pytest -q`
6. `ruff check src tests tools`
