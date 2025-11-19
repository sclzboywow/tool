"""Fingerprint tool JavaScript assets and emit a manifest for templating."""

import hashlib
import json
from pathlib import Path
from typing import Dict

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TOOLS_JS_DIR = STATIC_DIR / "js" / "tools"
MANIFEST_PATH = STATIC_DIR / "manifest.json"


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()[:12]


def _write_hashed_copy(source: Path, hashed_name: str) -> Path:
    hashed_path = source.with_name(hashed_name)
    if not hashed_path.exists() or hashed_path.read_bytes() != source.read_bytes():
        hashed_path.write_bytes(source.read_bytes())
    return hashed_path


def _cleanup_old_hashes(source: Path, keep_name: str) -> None:
    stem = source.stem
    suffix = source.suffix
    for candidate in source.parent.glob(f"{stem}.*{suffix}"):
        if candidate.name != keep_name:
            candidate.unlink()


def generate_manifest() -> Dict[str, str]:
    if not TOOLS_JS_DIR.exists():
        raise SystemExit(f"Tools JS directory not found: {TOOLS_JS_DIR}")

    manifest: Dict[str, str] = {}
    for script_path in sorted(TOOLS_JS_DIR.glob("*.js")):
        asset_hash = _hash_file(script_path)
        hashed_name = f"{script_path.stem}.{asset_hash}{script_path.suffix}"
        _write_hashed_copy(script_path, hashed_name)
        _cleanup_old_hashes(script_path, keep_name=hashed_name)
        manifest[f"js/tools/{script_path.name}"] = f"js/tools/{hashed_name}"

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    return manifest


def main() -> None:
    manifest = generate_manifest()
    print("Generated manifest:")
    for original, hashed in manifest.items():
        print(f"  {original} -> {hashed}")


if __name__ == "__main__":
    main()

