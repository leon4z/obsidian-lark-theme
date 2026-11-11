#!/usr/bin/env python3
"""Build a local installation ZIP. This script never publishes anything."""
from pathlib import Path
import zipfile

from check import ROOT, check


def main():
    manifest = check()
    folder = manifest["name"]
    destination = ROOT / "dist" / f"Lark-{manifest['version']}.zip"
    destination.parent.mkdir(exist_ok=True)
    files = [ROOT / name for name in ["theme.css", "manifest.json", "LICENSE"]]
    files.extend(p for p in (ROOT / "assets").rglob("*") if p.is_file())
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            assert not path.is_symlink(), path
            archive.write(path, Path(folder) / path.relative_to(ROOT))
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert archive.read(f"{folder}/theme.css") == (ROOT / "theme.css").read_bytes()
        assert archive.read(f"{folder}/LICENSE") == (ROOT / "LICENSE").read_bytes()
        assert archive.read(f"{folder}/assets/LICENSE-lucide") == (ROOT / "assets/LICENSE-lucide").read_bytes()
        assert "ISC License" in archive.read(f"{folder}/theme.css").decode()
    print(f"Local package: {destination}")


if __name__ == "__main__":
    main()
