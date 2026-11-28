"""The settings REAPER keeps in reaper.ini come back after a render process quits."""

from pathlib import Path

from mps import render

INI = (
    "[reaper]\r\n"
    "afxcfg=0\r\n"
    "lastproject=C:\\work\\song.rpp\r\n"
    "maxrecent=50\r\n"
    "[Recent]\r\n"
    "recent01=C:\\work\\song.rpp.mps-render.json.empty.rpp\r\n"
    "recent02=C:\\work\\song.rpp\r\n"
    "recent03=C:\\work\\other.rpp\r\n"
    "[REAPER-fxadd]\r\n"
    "x=1\r\n"
)


def _write(tmp_path: Path, text: str) -> Path:
    p = tmp_path / "reaper.ini"
    p.write_bytes(text.encode("utf-8"))
    return p


def test_last_project_reads_the_reaper_section(tmp_path):
    assert render.last_project(_write(tmp_path, INI)) == "C:\\work\\song.rpp"


def test_restore_puts_back_the_last_project_and_drops_the_temporary_entry(tmp_path):
    temp = Path("C:\\work\\song.rpp.mps-render.json.empty.rpp")
    after_render = INI.replace("lastproject=C:\\work\\song.rpp", f"lastproject={temp}")
    p = _write(tmp_path, after_render)
    changed = render.restore_after_render(p, "C:\\work\\before.rpp", temp)
    text = p.read_bytes().decode("utf-8")
    assert changed == {"lastproject_restored": True, "recent_removed": 1}
    assert "lastproject=C:\\work\\before.rpp\r\n" in text
    assert "empty.rpp" not in text
    # the other entries move up with no gap, and nothing else changes
    assert "recent01=C:\\work\\song.rpp\r\nrecent02=C:\\work\\other.rpp\r\n[REAPER-fxadd]" in text
    assert text.startswith("[reaper]\r\nafxcfg=0\r\n")
    assert text.endswith("x=1\r\n")


def test_restore_also_drops_temporary_entries_left_by_earlier_renders(tmp_path):
    old = INI.replace("recent03=C:\\work\\other.rpp", "recent03=D:\\old\\x.rpp.mps-render.json.empty.rpp")
    p = _write(tmp_path, old)
    changed = render.restore_after_render(p, "C:\\work\\song.rpp", Path("C:\\work\\song.rpp.mps-render.json.empty.rpp"))
    text = p.read_bytes().decode("utf-8")
    assert changed == {"lastproject_restored": False, "recent_removed": 2}
    assert "[Recent]\r\nrecent01=C:\\work\\song.rpp\r\n[REAPER-fxadd]" in text


def test_restore_leaves_an_unchanged_file_alone(tmp_path):
    clean = INI.replace("recent01=C:\\work\\song.rpp.mps-render.json.empty.rpp\r\n", "")
    p = _write(tmp_path, clean)
    before = p.read_bytes()
    changed = render.restore_after_render(p, "C:\\work\\song.rpp", Path("C:\\work\\song.rpp.mps-render.json.empty.rpp"))
    assert changed == {"lastproject_restored": False, "recent_removed": 0}
    assert p.read_bytes() == before


def test_restore_removes_a_last_project_that_was_not_there_before(tmp_path):
    p = _write(tmp_path, INI)
    changed = render.restore_after_render(p, None, Path("C:\\elsewhere.rpp"))
    assert changed["lastproject_restored"] is True
    assert "lastproject" not in p.read_bytes().decode("utf-8")


def test_non_utf8_bytes_survive(tmp_path):
    p = tmp_path / "reaper.ini"
    p.write_bytes(b"[reaper]\r\nname=caf\xe9\r\nlastproject=a.rpp\r\n")
    render.restore_after_render(p, "b.rpp", Path("x.rpp"))
    assert p.read_bytes() == b"[reaper]\r\nname=caf\xe9\r\nlastproject=b.rpp\r\n"
