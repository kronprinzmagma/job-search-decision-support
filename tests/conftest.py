"""Gemeinsame Fixtures: jeder Test arbeitet in einer Temp-Kopie mit frisch erzeugten Demo-Daten."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
HEUTE = "2025-04-25"
KOPIEREN = ("scripts", "spec", "persona", "vorlagen", "demo", "AGENTS.md")


def _kopie(ziel: Path) -> Path:
    for name in KOPIEREN:
        q = REPO / name
        if q.is_dir():
            shutil.copytree(q, ziel / name, ignore=shutil.ignore_patterns("__pycache__"))
        elif q.exists():
            shutil.copy2(q, ziel / name)
    subprocess.run([sys.executable, str(ziel / "scripts" / "init_demo.py"), "--ziel", str(ziel)],
                   check=True, capture_output=True, text=True)
    return ziel


@pytest.fixture(scope="session")
def demo_vorlage(tmp_path_factory):
    """Einmal je Testlauf erzeugt; Tests bekommen davon je eine eigene Kopie."""
    return _kopie(tmp_path_factory.mktemp("demo_vorlage"))


@pytest.fixture
def demo(demo_vorlage, tmp_path):
    ziel = tmp_path / "repo"
    shutil.copytree(demo_vorlage, ziel)
    return ziel


def run(demo: Path, skript: str, *args, heute: str = HEUTE, jetzt: str | None = None, eingabe: str | None = None):
    env = {**os.environ, "JC_HEUTE": heute, "PYTHONDONTWRITEBYTECODE": "1"}
    if jetzt:
        env["JC_JETZT"] = jetzt
    return subprocess.run([sys.executable, str(demo / "scripts" / skript), *map(str, args)], cwd=demo, env=env,
                          capture_output=True, text=True, input=eingabe, timeout=120)
