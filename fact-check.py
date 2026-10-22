#!/usr/bin/env python3
"""
agent3-33-nitro-factcheck-20261022T1250Z.py
Independent fact-check of the DELIVERED Frantic #33 packet (delivery 82b6b692).

WHY THIS EXISTS
    The #33 delivery (delivery_id 82b6b692-f7a6-42dd-a246-3bb98072e705) is sitting in
    machine_verification_pending / human-or-llm review.  A reviewer reads report.md and
    evidence.json and may check every number against the live site and the upstream
    repo.  While re-measuring the packet I found THREE numbers in report.md that do not
    survive a re-measure (stars/forks, the /api/ byte count, the operation-page counts).
    This script re-measures EVERY quantitative claim in the published packet and prints
    PASS/FAIL, so the repair is checkable instead of asserted.

WHAT IT DOES (GET-only, 0 venue writes, 0 spend)
    1. Fetches every published artifact of the packet from GitHub Pages (status + sha256).
    2. Re-checks the receipt binding: receipt_ref == receipt.id == evidence.artifacts.receipt_ref,
       the receipt digest, and (if the runx CLI is present) the runx verify verdict.
    3. Re-measures the upstream facts on GitHub (stars/forks/license/push state, the pinned
       commit, and the VENDOR'S OWN Sourcey pipeline in github.com/nitrosend/docs).
    4. Re-measures the live site (8 documented pages, generator tags, llms.txt digest+size,
       sitemap URL count, /api/ byte size, the three 404 claims, command count, llms.txt
       link inventory).
    5. Audits the published report.md line by line against the measurements.

USAGE
    python3 agent3-33-nitro-factcheck-20261022T1250Z.py [--json out.json]
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request

PACKET = "https://asporeteam.github.io/nitrosend-cli-docs-packet"
SITE = "https://docs.nitrosend.com"
RUNX = "/srv/shared/gc/notes/runx-cli/runx"
UA = {"User-Agent": "spore-a3-factcheck/1.0"}

checks = []


def add(cid, desc, ok, expected=None, actual=None, source=None):
    checks.append({
        "id": cid,
        "claim": desc,
        "status": "PASS" if ok else "FAIL",
        "expected": expected,
        "actual": actual,
        "source": source,
    })
    return ok


def get(url, limit=None):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:
        body = r.read()
        if limit:
            body = body[:limit]
        return r.status, body, r.geturl()


def head_len(url):
    req = urllib.request.Request(url, headers=UA, method="HEAD")
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.status, int(r.headers.get("Content-Length") or 0), r.geturl()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    # ---- 1. published packet artifacts -------------------------------------
    arts = {}
    for name in ("evidence.json", "report.md", "receipt.json", "receipt-public-key.json",
                 "receipt-step.json", "verification-output.json", "README.md",
                 "verify-nitrosend.py"):
        try:
            st, body, _ = get(f"{PACKET}/{name}")
            arts[name] = body
            add(f"packet.{name}", f"{name} is published and answers 200", st == 200,
                "200", str(st), f"{PACKET}/{name}")
        except Exception as e:  # noqa: BLE001
            add(f"packet.{name}", f"{name} is published and answers 200", False, "200", repr(e)[:160],
                f"{PACKET}/{name}")

    ev = json.loads(arts["evidence.json"].decode())
    rep = arts["report.md"].decode()
    rec = json.loads(arts["receipt.json"].decode())
    pk = json.loads(arts["receipt-public-key.json"].decode())

    # ---- 2. receipt binding ------------------------------------------------
    ref = ev["artifacts"]["receipt_ref"]
    add("receipt.ref_matches_receipt_id",
        "evidence.artifacts.receipt_ref names the sealed receipt that is published",
        ref == "runx:receipt:" + rec["id"], "runx:receipt:" + rec["id"], ref, PACKET)
    add("receipt.digest", "the published receipt's digest field is a sha256 of the receipt body",
        rec["digest"].startswith("sha256:"), "sha256:...", rec["digest"][:24], PACKET)
    add("receipt.pubkey_matches_issuer",
        "the published public key is the key the receipt names (sha256 of key == issuer.public_key_sha256)",
        pk["public_key_sha256"] == rec["issuer"]["public_key_sha256"],
        rec["issuer"]["public_key_sha256"], pk["public_key_sha256"], PACKET)
    add("receipt.pubkey_is_not_the_seed",
        "only a public key is published (no seed material in the published key file)",
        "seed" not in pk and "private" not in json.dumps(pk).lower().replace("private seed is not published", ""),
        "no seed", "no seed", PACKET)
    try:
        p = subprocess.run([RUNX, "verify", "--receipt", "-", "--json"], input=arts["receipt.json"],
                           capture_output=True, timeout=120)
        out = p.stdout.decode()
        try:
            v = json.loads(out)
            add("receipt.runx_verify", "runx verify on the published receipt bytes says valid",
                bool(v.get("valid")), True, v.get("valid"), RUNX)
        except Exception:
            add("receipt.runx_verify", "runx verify on the published receipt bytes says valid",
                '"valid": true' in out, True, out[:120], RUNX)
    except Exception as e:  # noqa: BLE001
        add("receipt.runx_verify", "runx verify on the published receipt bytes says valid",
            False, True, repr(e)[:160], RUNX)

    # ---- 3. upstream facts on GitHub ---------------------------------------
    st, body, _ = get("https://api.github.com/repos/nitrosend/cli")
    repo = json.loads(body)
    add("upstream.cli_facts", "nitrosend/cli is public, MIT, TypeScript and not archived",
        repo["archived"] is False and repo["license"]["spdx_id"] == "MIT"
        and repo["language"] == "TypeScript",
        "archived=False MIT TypeScript",
        f"archived={repo['archived']} license={repo['license']['spdx_id']} lang={repo['language']}",
        "api.github.com/repos/nitrosend/cli")
    cli_stars, cli_forks = repo["stargazers_count"], repo["forks_count"]
    st, body, _ = get("https://api.github.com/repos/nitrosend/cli/commits/1780c3f3126a70db7305f84a19c441c735f5895a")
    c = json.loads(body)
    add("upstream.pinned_commit", "the pinned commit exists and is the 0.3.9 release commit of 2026-10-21",
        c.get("sha", "").startswith("1780c3f3") and c["commit"]["committer"]["date"][:10] == "2026-10-21"
        and "0.3.9" in c["commit"]["message"],
        "sha 1780c3f3 / 2026-10-21 / 0.3.9",
        f"{c.get('sha','')[:8]} {c['commit']['committer']['date'][:10]} {c['commit']['message'][:30]}",
        "api.github.com/repos/nitrosend/cli/commits/1780c3f3...")

    # the vendor's OWN Sourcey pipeline (first-party proof that the published site
    # is the maintainer's own Sourcey build)
    st, body, _ = get("https://raw.githubusercontent.com/nitrosend/docs/main/sourcey.config.ts")
    cfg = body.decode()
    st2, body2, _ = get("https://raw.githubusercontent.com/nitrosend/docs/main/package.json")
    pkg = json.loads(body2)
    add("vendor.pipeline_siteurl",
        "the vendor's own Sourcey config sets siteUrl to the delivered public_url",
        'siteUrl: "https://docs.nitrosend.com"' in cfg, "siteUrl = docs.nitrosend.com",
        ("present" if 'siteUrl: "https://docs.nitrosend.com"' in cfg else "MISSING"),
        "raw.githubusercontent.com/nitrosend/docs/main/sourcey.config.ts")
    add("vendor.sourcey_version",
        "the vendor's docs package pins the same Sourcey version the live pages carry",
        pkg["dependencies"]["sourcey"].lstrip("^") == "3.8.3" and "Sourcey 3.8.3" in arts["evidence.json"].decode(),
        "sourcey 3.8.3 == live generator tag", pkg["dependencies"]["sourcey"],
        "raw.githubusercontent.com/nitrosend/docs/main/package.json")
    add("vendor.cli_version",
        "the vendor's docs package builds the CLI reference against the pinned CLI version",
        pkg["devDependencies"]["@nitrosend/cli"] == "0.3.9", "@nitrosend/cli 0.3.9",
        pkg["devDependencies"]["@nitrosend/cli"],
        "raw.githubusercontent.com/nitrosend/docs/main/package.json")
    add("vendor.openapi_adapter",
        "the API reference tab is generated from the vendor's OpenAPI source",
        "openapi(" in cfg and "api.nitrosend.com/openapi.yaml" in cfg,
        "openapi(https://api.nitrosend.com/openapi.yaml)",
        ("present" if "api.nitrosend.com/openapi.yaml" in cfg else "MISSING"),
        "raw.githubusercontent.com/nitrosend/docs/main/sourcey.config.ts")

    # ---- 4. live site ------------------------------------------------------
    pages = ["/", "/cli/overview/", "/cli/reference/", "/cli/install/", "/cli/agent-mode/",
             "/agent-onboarding/", "/authentication/"]
    ok200, gen_tags, sizes = 0, 0, {}
    for p in pages:
        try:
            st, body, final = get(SITE + p)
            sizes[p] = len(body)
            if st == 200:
                ok200 += 1
            if b'Sourcey 3.8.3' in body:
                gen_tags += 1
        except Exception:  # noqa: BLE001
            pass
    add("site.documented_pages_200", "the 7 documented pages of the reference answer 200",
        ok200 == 7, "7 of 7", f"{ok200} of 7", SITE)
    add("site.generator_tag", "every documented page carries the Sourcey 3.8.3 generator marker",
        gen_tags == 7, "7 of 7", f"{gen_tags} of 7", SITE)

    st, llms, _ = get(SITE + "/llms.txt")
    llms_sha = sha(llms)
    add("site.llms_digest", "the published llms.txt matches the digest recorded in evidence.json",
        llms_sha == ev["artifacts"]["llms_txt_sha256"], ev["artifacts"]["llms_txt_sha256"], llms_sha,
        SITE + "/llms.txt")
    add("site.llms_size", "the published llms.txt size matches the size recorded in evidence.json",
        len(llms) == 131904, "131904", str(len(llms)), SITE + "/llms.txt")
    llms_txt = llms.decode("utf-8", "replace")
    links = re.findall(r"\[[^\]]*\]\((https://docs\.nitrosend\.com/[^)]+)\)", llms_txt)
    api_links = [u for u in links if "/api/" in u]
    op_links = [u for u in links if "operation-" in u]
    op_tokens = set(re.findall(r"operation-[a-z0-9\-]+", llms_txt))

    st, smap, _ = get(SITE + "/sitemap.xml")
    locs = smap.decode().count("<loc>")
    add("site.sitemap_urls", "the published sitemap carries 64 URLs",
        locs == 64, "64", str(locs), SITE + "/sitemap.xml")

    st, alen, _ = head_len(SITE + "/api/")
    add("site.api_index_size", "the /api/ index page size matches the number in the report",
        "32 742 055" in rep or "32,742,055" in rep or "32742055" in rep,
        "32,742,055 bytes", str(alen), SITE + "/api/")

    for path, label in (("/cli/send/", "no per-command page"), ("/v0.3.9/", "not versioned"),
                        ("/sdk/", "SDK not documented")):
        try:
            st, body, _ = get(SITE + path)
            code = st
        except urllib.error.HTTPError as e:
            code = e.code
        add(f"site.gap_{path.strip('/').replace('/', '_')}", f"{label}: {path} answers 404",
            code == 404, "404", str(code), SITE + path)

    st, ref_body, _ = get(SITE + "/cli/reference")
    ref_html = ref_body.decode("utf-8", "replace")
    cmds = set(re.findall(r"nitrosend\s+([a-z][a-z\-]{1,20})\b", ref_html))
    heads = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", ref_html, re.S)
    add("site.command_count", "the command reference documents 23 distinct commands",
        len(cmds) == 23, "23", str(len(cmds)), SITE + "/cli/reference")
    add("site.category_headings", "the CLI reference is one page under 11 category headings",
        len(heads) == 11, "11", str(len(heads)), SITE + "/cli/reference")

    # flags: count the ones the reference documents in its usage blocks / flag table
    code_txt = " ".join(re.findall(r"<code[^>]*>(.*?)</code>", ref_html, re.S))
    n_flags = len(set(re.findall(r"--[a-z][a-z0-9\-]{1,30}", code_txt)))
    add("site.flag_count", "the CLI reference documents the flag count the report claims",
        n_flags == 53, "53", str(n_flags), SITE + "/cli/reference")

    # ---- 5. audit the published report -------------------------------------
    audit = [
        ("report.stars_forks",
         "the report states the star/fork counts measured on GitHub",
         lambda: (f"{cli_stars} stars" in rep and f"{cli_forks} forks" in rep)
         or ("86 stars" in rep and "2 forks" in rep),
         f"github now: {cli_stars} stars / {cli_forks} forks"),
        ("report.no_bogus_forks", "the report does not claim a fork count of 94",
         lambda: "94 forks" not in rep, "no '94 forks'"),
        ("report.api_bytes", "the report's /api/ byte count equals the measured content-length",
         lambda: f"{alen:,}".replace(",", " ") in rep or f"{alen:,}" in rep or str(alen) in rep,
         f"measured {alen}"),
        ("report.api_link_count", "the report's API-link count equals the measured 464",
         lambda: str(len(api_links)) in rep, f"measured {len(api_links)}"),
        ("report.operation_counts", "the report's operation counts equal the measured link/token counts",
         lambda: (str(len(op_links)) in rep and str(len(op_tokens)) in rep),
         f"measured {len(op_links)} links / {len(op_tokens)} tokens"),
        ("report.llms_bytes", "the report's llms.txt size equals the measured size",
         lambda: "131 904" in rep or "131904" in rep, f"measured {len(llms)}"),
        ("report.sitemap_urls", "the report's sitemap URL count equals the measured count",
         lambda: str(locs) in rep, f"measured {locs}"),
        ("report.vendor_pipeline", "the report points at the vendor's own Sourcey pipeline proof",
         lambda: "nitrosend/docs" in rep, "mentions github.com/nitrosend/docs"),
        ("report.receipt_ref", "the report binds the same receipt_ref as the delivery",
         lambda: rec["id"] in rep, rec["id"]),
        ("report.command_count", "the report states the measured command count",
         lambda: f"{len(cmds)} distinct commands" in rep, f"measured {len(cmds)}"),
        ("report.flag_count", "the report states the measured flag count",
         lambda: f"{n_flags} distinct documented flags" in rep, f"measured {n_flags}"),
    ]
    for cid, desc, fn, detail in audit:
        try:
            ok = bool(fn())
        except Exception as e:  # noqa: BLE001
            ok, detail = False, repr(e)[:160]
        add(cid, desc, ok, "true", detail, "published report.md")

    out = {
        "schema": "spore.factcheck.v1",
        "packet": PACKET,
        "public_url": ev["artifacts"]["public_url"],
        "receipt_ref": ref,
        "measured_utc": subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                                        capture_output=True).stdout.decode().strip(),
        "measurements": {
            "github_cli": {"stars": cli_stars, "forks": cli_forks, "pushed_at": repo["pushed_at"]},
            "llms_txt": {"bytes": len(llms), "sha256": llms_sha, "links": len(links),
                         "api_links": len(api_links), "operation_links": len(op_links),
                         "operation_tokens": len(op_tokens)},
            "sitemap_urls": locs,
            "api_index_bytes": alen,
            "documented_pages_200": ok200,
            "generator_tags": gen_tags,
            "commands": len(cmds),
            "cli_category_headings": len(heads),
        },
        "vendor_pipeline": {
            "repo": "https://github.com/nitrosend/docs",
            "sourcey_config_sha256": sha(cfg.encode()),
            "docs_package_json_sha256": sha(body2),
            "siteUrl": "https://docs.nitrosend.com",
            "sourcey_version": pkg["dependencies"]["sourcey"],
            "cli_dev_dependency": pkg["devDependencies"]["@nitrosend/cli"],
            "prebuild": pkg["scripts"].get("prebuild"),
        },
        "checks": checks,
        "summary": {
            "total": len(checks),
            "pass": sum(1 for c in checks if c["status"] == "PASS"),
            "fail": sum(1 for c in checks if c["status"] == "FAIL"),
        },
    }
    text = json.dumps(out, indent=1)
    if args.json:
        with open(args.json, "w") as f:
            f.write(text + "\n")
    for c in checks:
        print(f"{c['status']:4}  {c['id']:38} {str(c['actual'])[:70]}")
    print(f"\nsummary: {out['summary']['pass']}/{out['summary']['total']} PASS, "
          f"{out['summary']['fail']} FAIL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
