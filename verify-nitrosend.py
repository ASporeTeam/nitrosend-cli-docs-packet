#!/usr/bin/env python3
"""Governed validation run for the published Sourcey documentation site of
Nitrosend (Frantic bounty #33).

Fetches the published site over plain HTTPS (the company's own registered
domain), checks that every page a reviewer would open answers 200, spot-checks
the documented API/CLI surface against the rendered pages, and recomputes the
digest of the llms.txt index and of the pinned upstream CLI repository file.
Prints one JSON object on stdout.  No writes, no spending.
"""
import hashlib
import json
import re
import os
import sys
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) spore-agent3-nitrosend-verify/1.0"

REPO = "nitrosend/cli"
COMMIT = "1780c3f3126a70db7305f84a19c441c735f5895a"
RAW_PACKAGE = "https://raw.githubusercontent.com/%s/%s/package.json" % (REPO, COMMIT)
RAW_LICENSE = "https://raw.githubusercontent.com/%s/%s/LICENSE" % (REPO, COMMIT)

PAGES = [
    "/",
    "/cli/overview/",
    "/cli/reference/",
    "/cli/install/",
    "/cli/agent-mode/",
    "/agent-onboarding/",
    "/authentication/",
    "/llms.txt",
]

SPOT_CHECKS = [
    ("/", "Nitrosend", "the landing page names the documented product"),
    ("/", "sourcey", "the landing page carries the Sourcey generator assets"),
    ("/cli/overview/", "nitrosend", "the CLI overview documents the nitrosend CLI"),
    ("/cli/reference/", "Command reference", "the CLI reference page is the command reference"),
    ("/cli/reference/", "nitrosend send", "the command reference documents the send command"),
    ("/cli/install/", "npm", "the install page documents how to install the CLI"),
    ("/agent-onboarding/", "MCP", "the agent onboarding page documents the agent path"),
    ("/llms.txt", "Nitrosend", "llms.txt is the agent-readable index of the reference"),
    ("/llms.txt", "operation-", "llms.txt lists the generated API operation pages"),
]


def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:  # noqa: BLE001 - a transport error is a fact
        return 0, ("error: %s" % exc).encode()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    base = os.environ.get("RUNX_INPUT_BASE_URL") or "https://docs.nitrosend.com"
    base = base.rstrip("/")

    page_results = []
    for p in PAGES:
        status, body = fetch(base + p)
        gen = ""
        m = None
        import re
        m = re.search(rb'<meta name="generator" content="([^"]*)"', body[:4000])
        if m:
            gen = m.group(1).decode()
        page_results.append({"path": p, "status": status, "bytes": len(body),
                             "generator": gen or None})

    checks = []
    for path, needle, why in SPOT_CHECKS:
        status, body = fetch(base + path)
        text = body.decode("utf-8", "replace")
        checks.append({"path": path, "needle": needle, "why": why,
                       "http_status": status, "found": needle in text})

    artifacts = {}
    status, body = fetch(RAW_PACKAGE)
    if status == 200:
        artifacts["package.json @ " + COMMIT] = {"url": RAW_PACKAGE,
                                                 "sha256": sha256_bytes(body),
                                                 "bytes": len(body)}
    status, body = fetch(RAW_LICENSE)
    if status == 200:
        artifacts["LICENSE @ " + COMMIT] = {"url": RAW_LICENSE,
                                            "sha256": sha256_bytes(body),
                                            "bytes": len(body)}
    status, body = fetch(base + "/llms.txt")
    if status == 200:
        artifacts["published llms.txt"] = {"url": base + "/llms.txt",
                                           "sha256": sha256_bytes(body),
                                           "bytes": len(body)}
        text = body.decode("utf-8", "replace")
        operations = sorted({m for m in re.findall(r"operation-[a-z0-9-]+", text)})
        api_pages = text.count("nitrosend.com/api/")
        cli_pages = text.count("nitrosend.com/cli/")
    else:
        operations = []
        api_pages = 0
        cli_pages = 0

    result = {
        "base_url": base,
        "target_repo": "https://github.com/" + REPO,
        "pinned_commit": COMMIT,
        "pages_checked": len(page_results),
        "pages_ok": sum(1 for p in page_results if p["status"] == 200),
        "page_results": page_results,
        "spot_checks_total": len(checks),
        "spot_checks_passed": sum(1 for c in checks if c["found"] and c["http_status"] == 200),
        "spot_checks": checks,
        "documented_api_pages": api_pages,
        "documented_cli_pages": cli_pages,
        "documented_operations": len(operations),
        "artifacts": artifacts,
        "verdict": "PASS" if (all(p["status"] == 200 for p in page_results)
                               and all(c["found"] for c in checks)) else "FAIL",
    }
    print(json.dumps({"message": json.dumps(result, sort_keys=True)}))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
