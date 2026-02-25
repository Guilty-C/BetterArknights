# is_auto (M0 scaffold)

明日方舟肉鸽(IS)自动化项目 M0 脚手架：提供可运行 CLI、契约校验、证据链目录与最小 smoke 闭环（dummy driver）。

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
python -m is_auto --help
is_auto smoke --out runs
python tools/acceptance_scaffold.py
```
