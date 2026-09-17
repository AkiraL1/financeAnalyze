from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from urllib.parse import urlparse

_ALLOWED_HOSTS = {
    "www.cmegroup.com",
    "cmegroup.com",
    "www.cftc.gov",
    "cftc.gov",
    "publicreporting.cftc.gov",
    "home.treasury.gov",
    "www.treasury.gov",
    "finance.yahoo.com",
    "www.ice.com",
    "www.federalreserve.gov",
    "www.coingecko.com",
    "alternative.me",
}

_MAX_CHARS = 4000


def host_allowed(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return False
    host = (parsed.hostname or "").lower()
    return host in _ALLOWED_HOSTS


def html_snapshot(markup: str, url: str, limit: int = _MAX_CHARS) -> str:
    cleaned = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", markup)
    refs: list[str] = []
    pattern = re.compile(r"(?is)<(h[1-3]|a|td|th|p|li|title|span)[^>]*>(.*?)</\1>")
    for index, match in enumerate(pattern.finditer(cleaned), start=1):
        inner = html.unescape(re.sub(r"<[^>]+>", " ", match.group(2)))
        inner = re.sub(r"\s+", " ", inner).strip()
        if not inner:
            continue
        refs.append(f"[ref={index} tag={match.group(1)}] {inner[:180]}")
        if len(refs) >= 80:
            break
    body = "\n".join(refs) if refs else re.sub(r"<[^>]+>", " ", cleaned)
    body = re.sub(r"\s+", " ", body).strip() if not refs else body
    return f"url={url}\n{body[:limit]}"


def snapshot_url(url: str, *, timeout: int = 20) -> dict[str, str]:
    if not host_allowed(url):
        return {
            "ok": "false",
            "engine": "blocked",
            "url": url,
            "snapshot": "域名不在交易所/监管白名单，拒绝打开。",
        }
    cli = shutil.which("ego-browser")
    if cli:
        try:
            return _ego_snapshot(cli, url, timeout)
        except Exception as exc:  # noqa: BLE001 - fallback to HTTP
            http = _http_snapshot(url, timeout)
            http["engine"] = f"http-fallback:{type(exc).__name__}"
            return http
    return _http_snapshot(url, timeout)


def _ego_snapshot(cli: str, url: str, timeout: int) -> dict[str, str]:
    script = (
        "const task = await useOrCreateTaskSpace('finance desk snapshot')\n"
        f"await openOrReuseTab({json.dumps(url)}, {{ wait: true, timeout: {timeout} }})\n"
        "cliLog(await snapshotText({ scope: 'only_within_viewport' }))\n"
    )
    proc = subprocess.run(
        [cli, "nodejs"],
        input=script,
        capture_output=True,
        text=True,
        timeout=timeout + 15,
        check=False,
    )
    text = (proc.stdout or proc.stderr or "").strip()
    if proc.returncode != 0 or not text:
        raise RuntimeError(text[:240] or f"exit {proc.returncode}")
    return {
        "ok": "true",
        "engine": "ego-browser",
        "url": url,
        "snapshot": text[:_MAX_CHARS],
    }


def _http_snapshot(url: str, timeout: int) -> dict[str, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "financeAnalyze-desk/0.1"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            final = response.geturl()
            if not host_allowed(final):
                return {
                    "ok": "false",
                    "engine": "http",
                    "url": url,
                    "snapshot": "重定向目标不在白名单。",
                }
            raw = response.read(200_000).decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        return {
            "ok": "false",
            "engine": "http",
            "url": url,
            "snapshot": f"抓取失败：{type(exc).__name__}",
        }
    return {
        "ok": "true",
        "engine": "http-snapshot",
        "url": final,
        "snapshot": html_snapshot(raw, final),
    }
