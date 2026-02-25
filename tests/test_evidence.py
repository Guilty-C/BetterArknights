import json

from is_auto.core.evidence import append_event, create_episode_dir, create_run_dir, write_run_manifest


def test_evidence_files(tmp_path) -> None:
    run_dir = create_run_dir(tmp_path)
    episode = create_episode_dir(run_dir, 1)
    append_event(run_dir, episode, {"step": 1})
    write_run_manifest(run_dir, "abc")
    assert (run_dir / "metadata.jsonl").exists()
    assert (run_dir / "run_manifest.json").exists()
    data = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
    assert "profile_hash" in data
