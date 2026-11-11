#!/usr/bin/env python3
"""Validate local theme metadata and distribution assets; no dependencies."""
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]


def check():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    assert manifest["name"] == "Lark"
    assert manifest["author"] == "leon4z"
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
    assert manifest["minAppVersion"] == "1.14.4"
    css = (ROOT / "theme.css").read_text()
    assert not re.search(r"@import\b|url\(\s*['\"]?(?:https?:)?//", css)
    assert "Quiet" not in css
    assert "Copyright (c) 2026 s1dashu" in css
    assert "ISC License" in css and "Lucide Contributors" in css
    assert "--bold-weight: 600;" in css
    assert "--inline-title-weight: 500;" in css
    for level in range(1, 7):
        assert f"--h{level}-weight: 500;" in css
    license_text = (ROOT / "LICENSE").read_text()
    assert "MIT License" in license_text and "ISC License" not in license_text
    icon_license = (ROOT / "assets/LICENSE-lucide").read_text()
    assert "ISC License" in icon_license and "Lucide Contributors" in icon_license
    assert license_text.strip() in css
    assert icon_license.strip() in css
    assert "leon4z" in license_text and "s1dashu" in license_text
    for name in ["README.md", "README.zh-CN.md"]:
        path = ROOT / name
        text = path.read_text()
        assert "Quiet" not in text
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "#")):
                continue
            assert (path.parent / target.split("#")[0]).is_file(), (name, target)
    sizes = {}
    for name in ["screenshot.png", "screenshots/light.png", "screenshots/dark.png"]:
        data = (ROOT / name).read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n", name
        width, height = struct.unpack(">II", data[16:24])
        assert width > 0 and height > 0
        if name == "screenshot.png":
            assert (width, height) == (512, 288), (width, height)
        assert len(data) < 3_000_000, name
        sizes[name] = {"width": width, "height": height, "bytes": len(data)}
    print(json.dumps({"name": manifest["name"], "version": manifest["version"], "screenshots": sizes, "status": "passed"}, indent=2))
    return manifest


if __name__ == "__main__":
    check()
