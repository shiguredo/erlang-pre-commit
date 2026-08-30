"""GitHub Releases から efmt / elint バイナリをダウンロードする。"""

from __future__ import annotations

import hashlib
import os
import platform
import stat
import urllib.error
import urllib.request
from pathlib import Path

from erlang_pre_commit.versions import (
    CHECKSUMS,
    EFMT_RELEASE_TAG,
    EFMT_VERSION,
    ELINT_RELEASE_TAG,
    ELINT_VERSION,
)

_USER_AGENT = "shiguredo-erlang-pre-commit"


def rust_target() -> str:
    system = platform.system()
    machine = platform.machine().lower()

    if machine in ("amd64", "x86_64"):
        arch = "x86_64"
    elif machine in ("arm64", "aarch64"):
        arch = "aarch64"
    else:
        raise RuntimeError(
            f"Unsupported CPU architecture for erlang-pre-commit: {platform.machine()}"
        )

    if system == "Darwin":
        return f"{arch}-apple-darwin"
    if system == "Linux":
        return f"{arch}-unknown-linux-musl"
    raise RuntimeError(
        f"Unsupported OS for erlang-pre-commit: {system} (supported: macOS and Linux)"
    )


def release_asset_url(tool: str, version: str, release_tag: str, target: str) -> str:
    asset = f"{tool}-{version}.{target}"
    return f"https://github.com/sile/{tool}/releases/download/{release_tag}/{asset}"


def _expected_checksum(tool: str, target: str) -> str:
    try:
        return CHECKSUMS[tool][target]
    except KeyError as exc:
        raise RuntimeError(
            f"No prebuilt {tool} binary for target {target}. "
            f"Available: {', '.join(sorted(CHECKSUMS.get(tool, {})))}"
        ) from exc


def _bin_dir() -> Path:
    override = os.environ.get("ERLANG_PRE_COMMIT_BIN_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent / "_bins"


def ensure_binary(tool: str) -> Path:
    if tool == "efmt":
        version = EFMT_VERSION
        release_tag = EFMT_RELEASE_TAG
    elif tool == "elint":
        version = ELINT_VERSION
        release_tag = ELINT_RELEASE_TAG
    else:
        raise ValueError(f"Unknown tool: {tool}")

    target = rust_target()
    expected = _expected_checksum(tool, target)
    destination = _bin_dir() / f"{tool}-{version}-{target}"

    if destination.is_file() and _sha256_file(destination) == expected:
        return destination

    url = release_asset_url(tool, version, release_tag, target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = destination.with_suffix(".tmp")

    try:
        request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
        with urllib.request.urlopen(request) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Failed to download {tool} {version} for {target} from {url}: HTTP {exc.code}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Failed to download {tool} {version} for {target} from {url}: {exc}"
        ) from exc

    digest = hashlib.sha256(data).hexdigest()
    if digest != expected:
        raise RuntimeError(
            f"Checksum mismatch for {tool} {version} ({target}): expected {expected}, got {digest}"
        )

    tmp_path.write_bytes(data)
    tmp_path.chmod(tmp_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    tmp_path.replace(destination)
    return destination


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
