"""How `mps render` combines the render process's outcome, the file checks and the render standard."""

import json
import os
import stat
import sys
import types
from pathlib import Path

import pytest

import mps
from mps import audio, cli, render

STANDARD_RPP = """<REAPER_PROJECT 0.1 "7.86/x64" 1794772900
  RENDER_FILE "{wav}"
  RENDER_FMT 0 2 44100
  RENDER_1X 0 0
  RENDER_RANGE 0 0 2 1 500
  RENDER_DITHER 0
  RENDER_NORMALIZE 262144 0 0 0 0 1 1
  SAMPLERATE 44100 1 0
  <RENDER_CFG
    ZXZhdyAAAQ==
  >
>
"""


@pytest.fixture
def fake_render(monkeypatch, tmp_path):
    out = tmp_path / "out.wav"

    def run(returncode, file_ok=True, extra=(), rpp_text=None, exists=False, seen=None, record_project=None):
        if exists:
            out.write_bytes(b"keep")
        if record_project is not None:
            rec = {"project": {"path": str(record_project)}, "checks": [{"path": str(out)}]}
            (tmp_path / "out.render.json").write_text(json.dumps(rec), encoding="utf-8")
        project = tmp_path / "p.rpp"
        if rpp_text is not None:
            project.write_text(rpp_text.format(wav=str(out).replace("\\", "\\\\")), encoding="utf-8")

        def fake_project(project, timeout, **kw):
            out.write_bytes(b"")
            return {"ok": True, "returncode": returncode, "started": 0.0, "seen": seen}

        monkeypatch.setattr(render, "render_project", fake_project)
        monkeypatch.setattr(audio, "check", lambda path, **kw: {"ok": file_ok, "failures": [] if file_ok else ["x"]})
        return cli.main(["render", str(project), "--expect", str(out), *extra])

    return run


def result(capsys):
    return json.loads(capsys.readouterr().out)


def test_a_relative_project_path_still_finds_the_render_record(monkeypatch, tmp_path):
    work, elsewhere = tmp_path / "work", tmp_path / "elsewhere"
    work.mkdir()
    elsewhere.mkdir()
    (work / "p.rpp").write_text("<REAPER_PROJECT 0.1\n>\n", encoding="utf-8")
    sent = {}

    class FakeProcess:
        pid, returncode = 1, 0

        def __init__(self, cmd, env):
            sent["env"] = env
            log = Path(env["MPS_RENDER_LOG"])
            # the REAPER process works from another folder, so a relative path lands there
            target = log if log.is_absolute() else elsewhere / log
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps({"tempo": 90.0, "qn_seconds": 0.6666666667}), encoding="utf-8")

        def poll(self):
            return 0

    fake_windows = types.ModuleType("mps.windows")
    fake_windows.dialogs = lambda pid=None: []
    monkeypatch.setitem(sys.modules, "mps.windows", fake_windows)
    monkeypatch.setattr(mps, "windows", fake_windows, raising=False)
    monkeypatch.setattr(render.subprocess, "Popen", lambda cmd, env: FakeProcess(cmd, env))
    monkeypatch.setattr(render, "reaper_exe", lambda: Path("reaper.exe"))
    monkeypatch.chdir(tmp_path)
    res = render.render_project(Path("work") / "p.rpp", timeout=5)
    assert Path(sent["env"]["MPS_RENDER_LOG"]).is_absolute()
    assert res["seen"] == {"tempo": 90.0, "qn_seconds": 0.6666666667}


def test_normal_exit_with_good_files_is_ok(fake_render, capsys):
    assert fake_render(0) == 0
    r = result(capsys)
    assert r["ok"] and r["files_ok"] and not r["abnormal_exit"]


def test_abnormal_exit_with_good_files_is_not_ok(fake_render, capsys):
    assert fake_render(0xC000000D) == 1
    r = result(capsys)
    assert r["files_ok"] and r["abnormal_exit"] and not r["ok"]


def test_bad_files_are_not_ok(fake_render, capsys):
    assert fake_render(0, file_ok=False) == 1
    r = result(capsys)
    assert not r["files_ok"] and not r["ok"]


def test_existing_target_is_refused_without_overwrite(fake_render, capsys):
    assert fake_render(0, exists=True) == 1
    r = result(capsys)
    assert "existing" in r and "returncode" not in r


def test_overwrite_replaces_a_file_rendered_from_the_same_project(fake_render, tmp_path):
    assert fake_render(0, exists=True, extra=["--overwrite"], record_project=tmp_path / "p.rpp") == 0


def test_overwrite_refuses_a_file_without_a_record(fake_render, capsys, tmp_path):
    assert fake_render(0, exists=True, extra=["--overwrite"]) == 1
    r = result(capsys)
    assert "no render record" in r["refusals"][0] and "returncode" not in r
    assert (tmp_path / "out.wav").read_bytes() == b"keep"


def test_overwrite_refuses_a_file_rendered_from_another_project(fake_render, capsys, tmp_path):
    assert fake_render(0, exists=True, extra=["--overwrite"], record_project=tmp_path / "source.rpp") == 1
    assert "source.rpp" in result(capsys)["refusals"][0]
    assert (tmp_path / "out.wav").read_bytes() == b"keep"


def test_replace_names_a_file_to_replace_on_purpose(fake_render, tmp_path):
    assert fake_render(0, exists=True, extra=["--replace", str(tmp_path / "out.wav")]) == 0


def test_a_read_only_target_is_never_replaced(fake_render, capsys, tmp_path):
    out = tmp_path / "out.wav"
    out.write_bytes(b"keep")
    os.chmod(out, stat.S_IREAD)
    try:
        assert fake_render(0, extra=["--overwrite", "--replace", str(out)], record_project=tmp_path / "p.rpp") == 1
        assert "read-only" in result(capsys)["refusals"][0]
        assert out.read_bytes() == b"keep"
    finally:
        os.chmod(out, stat.S_IREAD | stat.S_IWRITE)


def test_a_relative_render_file_is_refused(fake_render, capsys):
    rel = STANDARD_RPP.replace('RENDER_FILE "{wav}"', 'RENDER_FILE "renders\\\\out.wav"')
    assert fake_render(0, rpp_text=rel) == 1
    assert "relative" in result(capsys)["refusals"][0]


def test_a_render_path_inherited_from_another_project_is_refused(fake_render, capsys, tmp_path):
    # a variant saved under a new name still renders to the file of the project it was copied from
    source = tmp_path / "source.wav"
    source.write_bytes(b"evidence")
    inherited = STANDARD_RPP.replace("{wav}", str(source).replace("\\", "\\\\"))
    assert fake_render(0, rpp_text=inherited, extra=["--overwrite"]) == 1
    r = result(capsys)
    assert any("doesn't name" in e for e in r["refusals"]) and "returncode" not in r
    assert source.read_bytes() == b"evidence"


def test_missing_media_is_refused_and_relative_media_resolve_from_the_project(fake_render, capsys, tmp_path):
    (tmp_path / "take.wav").write_bytes(b"")
    item = '  <TRACK\n    <ITEM\n      <SOURCE WAVE\n        FILE "{0}"\n      >\n    >\n  >\n'
    relative = STANDARD_RPP.replace("\n>\n", "\n" + item.format("take.wav") + ">\n")
    assert fake_render(0, rpp_text=relative) == 0
    assert result(capsys)["relative_media"] == ["take.wav"]
    missing = STANDARD_RPP.replace("\n>\n", "\n" + item.format("gone.wav") + ">\n")
    assert fake_render(0, rpp_text=missing, extra=["--overwrite"]) == 1
    assert "gone.wav" in result(capsys)["refusals"][0]


def test_the_record_keeps_the_absolute_project_path(fake_render, capsys, tmp_path):
    assert fake_render(0, rpp_text=STANDARD_RPP) == 0
    rec = json.loads((tmp_path / "out.render.json").read_text(encoding="utf-8"))
    assert os.path.isabs(rec["project"]["path"])


def test_standard_project_passes_and_writes_a_manifest(fake_render, capsys, tmp_path):
    assert fake_render(0, rpp_text=STANDARD_RPP) == 0
    r = result(capsys)
    assert r["standard"]["ok"] and r["expected_seconds"] == 2.5
    assert json.loads((tmp_path / "out.render.json").read_text(encoding="utf-8"))["settings"]["format"] == "wav32f"


def test_nonstandard_project_fails_unless_allowed(fake_render, capsys):
    wav24 = STANDARD_RPP.replace("ZXZhdyAAAQ==", "ZXZhdxgAAQ==")
    assert fake_render(0, rpp_text=wav24) == 1
    r = result(capsys)
    assert not r["standard"]["ok"] and "wav24" in r["standard"]["deviations"][0]
    assert fake_render(0, rpp_text=wav24, extra=["--allow-nonstandard", "--overwrite"]) == 0


def test_process_check_catches_a_render_at_the_wrong_tempo():
    settings = {"tempo": 90}
    assert cli.render_process_check({"seen": {"tempo": 90}}, settings)["ok"]
    wrong = cli.render_process_check({"seen": {"tempo": 120}}, settings)
    assert not wrong["ok"] and "120" in wrong["failure"]
    assert not cli.render_process_check({"seen": {"error": "the render script left no record"}}, settings)["ok"]
    assert cli.render_process_check({"seen": None}, settings) == {"ok": True, "checked": False}


def test_wrong_tempo_fails_the_render(fake_render, capsys):
    with_tempo = STANDARD_RPP.replace("SAMPLERATE 44100 1 0", "SAMPLERATE 44100 1 0\n  TEMPO 90 4 4 0")
    assert fake_render(0, rpp_text=with_tempo, seen={"tempo": 120}) == 1
    assert not result(capsys)["process_check"]["ok"]
    assert fake_render(0, rpp_text=with_tempo, seen={"tempo": 90}, extra=["--overwrite"]) == 0


def test_process_check_uses_the_quarter_note_length():
    settings = {"tempo": 104.4858}
    assert cli.render_process_check({"seen": {"tempo": 104.486, "qn_seconds": 60 / 104.4858}}, settings)["ok"]
    assert not cli.render_process_check({"seen": {"tempo": 104.486, "qn_seconds": 0.5}}, settings)["ok"]
    assert cli.render_process_check({"seen": {"tempo": 104.486}}, settings)["ok"]
