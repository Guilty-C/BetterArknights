# ARCHITECTURE (M0)

- **Perception**: `perception/page_id.py`，根据帧识别页面（M0 用 dummy 固定输出）。
- **Decision**: `decision/policy_v0.py`，对选项打分并产出 `action_t`。
- **Actuation**: `actuation/primitives.py`，动作原语 contract + dummy execute。
- **FSM**: `fsm/fsm.py`，状态机骨架（入口/开局/路线图/节点/结算）。
- **Evidence**: `core/evidence.py`，run/episode 目录、manifest、metadata、run.log。
