# SPDX-License-Identifier: Apache-2.0
import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/inspect_zw810.py"
spec = importlib.util.spec_from_file_location("inspect_zw810", SCRIPT)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def record(ordinal=0, count=1):
    return probe.DEVICE_MARKER + json.dumps({
        "name": "ZW810", "ordinal": ordinal, "visible_devices": count})


@pytest.mark.parametrize("output", ["", record(1, 2), record() + "\n" + record(), record(0, 0)])
def test_missing_wrong_or_ambiguous_device_is_rejected(output):
    with pytest.raises(ValueError):
        probe.parse_device(output, 0)


def test_existing_evidence_is_not_overwritten(tmp_path):
    marker = tmp_path / "environment.json"
    marker.write_text("prior evidence")
    with pytest.raises(SystemExit) as exc:
        probe.main(["--sdk", "/unused-sdk", "--out", str(tmp_path)])
    assert exc.value.code == 2
    assert marker.read_text() == "prior evidence"


def test_failed_build_does_not_execute_a_stale_binary(tmp_path, monkeypatch):
    calls = []
    (tmp_path / "ppu_device_info").write_text("stale output")

    def run(command, out, label, timeout):
        calls.append(label)
        return {"status": "failed" if label == "device-query-build" else "ok", "output": ""}

    monkeypatch.setattr(probe, "run", run)
    report = probe.inspect(tmp_path / "sdk", 0, tmp_path, 1)
    assert report["status"] == "unavailable"
    assert report["device"] is None
    assert "device-query" not in calls


def test_runtime_failure_is_not_a_successful_environment(tmp_path, monkeypatch):
    def run(command, out, label, timeout):
        if label == "device-query-build":
            (out / "ppu_device_info").touch()
        return {"status": "failed" if label == "device-query" else "ok", "output": record()}

    monkeypatch.setattr(probe, "run", run)
    report = probe.inspect(tmp_path / "sdk", 0, tmp_path, 1)
    assert report["status"] == "unavailable"
    assert report["device"] is None


def test_missing_profiler_does_not_hide_a_valid_runtime_query(tmp_path, monkeypatch):
    def run(command, out, label, timeout):
        if label == "device-query-build":
            (out / "ppu_device_info").touch()
        return {"status": "unavailable" if label in {"acu", "asys"} else "ok",
                "output": record() if label == "device-query" else ""}

    monkeypatch.setattr(probe, "run", run)
    report = probe.inspect(tmp_path / "sdk", 0, tmp_path, 1)
    assert report["status"] == "runtime_queried"
    assert report["device"]["name"] == "ZW810"
    assert report["tools"]["acu"]["status"] == "unavailable"
    assert report["kernel_execution"] == "not_performed"
