# WORKFLOW

## Branching
- 主干使用 `main` + 开发分支 `feature/*`。
- 两位开发者分别在各自 `feature/*` 分支开发，通过 PR 合并到 `main`。

## Commit Convention
- 使用前缀：`feat:` / `fix:` / `chore:`。
- 每次提交前必须运行：`python tools/acceptance_scaffold.py`。

## Milestones
- M0：脚手架、CLI、契约、证据链、smoke、验收脚本。
- M1：接入真实页面识别与简单策略闭环。
- M2：稳定性、回放审计、更多策略与设备适配。
