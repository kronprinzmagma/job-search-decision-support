"""Gruppe Einstellungen: Claude Code darf die Falldatei und die Ansichten nicht direkt bearbeiten."""
import json

from conftest import REPO


def test_falldatei_und_ansichten_sind_fuer_claude_code_gesperrt():
    einstellungen = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    deny = einstellungen["permissions"]["deny"]
    # Edit(...) deckt alle Datei-Werkzeuge ab (Edit, Write, NotebookEdit); Write(<pfad>) wuerde nie greifen
    assert "Edit(/data/pipeline.json)" in deny
    assert "Edit(/data/screening_log.json)" in deny
    assert "Edit(/views/**)" in deny
    assert not [r for r in deny if r.startswith("Write(")]
    # nichts, was das Lesen oder die Skripte sperrt
    assert not [r for r in deny if r.startswith(("Read", "Bash"))]
    assert (REPO / "data" / "pipeline.json").is_file() and (REPO / "data" / "screening_log.json").is_file()
    assert (REPO / "views").is_dir()


def test_konsistenz_check_laeuft_als_sessionstart_hook():
    einstellungen = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    befehle = [h["command"] for g in einstellungen["hooks"]["SessionStart"] for h in g["hooks"]]
    assert any("scripts/jobcoach.py" in b and "--pruefen" in b for b in befehle)
