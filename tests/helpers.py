"""Shared by the tests: where the scripts are, how to load one as a module and how to run one as a command."""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent
PLUGIN = ROOT / "plugins" / "poiesis-insight"
SKILL = PLUGIN / "skills" / "insight"
SCRIPTS = SKILL / "scripts"


def load(name: str):
    """A script of the plugin as a module, loaded from its file."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(script: str, *args: str, cwd: Path | str | None = None) -> subprocess.CompletedProcess:
    """Run a script the way the playbooks do: `python3 -I script.py ...`."""
    return subprocess.run([sys.executable, "-I", str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True, cwd=cwd)


def lab() -> Path | None:
    """The Poiesis Lab notebook's `fixtures` folder: the folder `POIESIS_LAB` names, then `~/Poiesis Lab`.
    None where neither holds it."""
    for folder in (os.environ.get("POIESIS_LAB"), Path.home() / "Poiesis Lab"):
        if folder and (Path(folder) / "fixtures" / "challenge-verdicts.json").is_file():
            return Path(folder) / "fixtures"
    return None
