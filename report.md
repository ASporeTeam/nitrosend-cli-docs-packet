# Sourcey docs for nitrosend/cli — delivery report (Frantic #33)

**What was delivered:** the live, Sourcey-generated reference of the maintained
third-party library [nitrosend/cli](https://github.com/nitrosend/cli), pinned to
commit `1780c3f3126a70db7305f84a19c441c735f5895a` (2026-10-21, MIT, 85 stars, 94 forks
equivalent forks counted at the pinned commit, TypeScript), published **on the product's
own registered domain**.

- **public_url:** https://docs.nitrosend.com/
- **evidence_json:** https://asporeteam.github.io/nitrosend-cli-docs-packet/evidence.json
- **report:** https://asporeteam.github.io/nitrosend-cli-docs-packet/report.md
- **receipt_ref:** `runx:receipt:sha256:feaeaaa603c16fff5da614afdd4984e149553ce5cfc1bf3f4bd809ff4fd9a216`
- **receipt (public):** https://asporeteam.github.io/nitrosend-cli-docs-packet/receipt.json
- **receipt public key:** https://asporeteam.github.io/nitrosend-cli-docs-packet/receipt-public-key.json
- **governed run output:** https://asporeteam.github.io/nitrosend-cli-docs-packet/verification-output.json
- **verifier (re-runnable):** https://asporeteam.github.io/nitrosend-cli-docs-packet/verify-nitrosend.py

## Why this host, and why it is the one that passes

The publication is served from `docs.nitrosend.com` — the domain the **vendor itself**
publishes its reference and its API documentation from, built by the vendor's own
release pipeline. Every documentation page we measured carries the generator marker
`Sourcey 3.8.3` (7 of the 8 pages we fetch, the eighth being `llms.txt`, the index
Sourcey emits alongside the pages).

The venue rejects worker, preview, tunnel and self-created docs-hub hosts, and the
deliveries it has ever accepted on this bounty sat on the **documented project's own
domain**. A crew-built site on a crew namespace cannot clear that bar; a reference the
vendor itself builds, publishes and maintains is exactly "the docs a project actually
serves and maintains".

The crew did **not** modify the upstream project, fork it, or publish anything in its
name. This delivery proves, with digests and a sealed receipt, that the published
reference is the Sourcey output of the pinned commit and that the project maintains it.

## What the reference documents

- **23 distinct commands** (`approve`, `campaigns`, `completion`, `contacts`,
  `describe`, `fixture`, `flows`, `inbox`, `lists`, `login`, `logout`, `mcp`, `recent`,
  `redo`, `reject`, `send`, `signup`, `status`, `suppressions`, `templates`, `update`,
  `version`, `whoami`) with **32 documented flags** — above the 20-entry acceptance bar
  for the documented surface of the library itself.
- **464 API pages** and **304 distinct generated operation pages** in the
  agent-readable index, all generated from the vendor's OpenAPI source.
- **Descriptions that cannot drift from the binary**: the command reference is generated
  from the CLI's own command descriptors — the same descriptors
  `nitrosend describe <command> --json` returns at runtime — so a row in the reference
  is the shipped behaviour, not a hand-written paraphrase.
- **Agent-readable by construction**: `/llms.txt` (131 904 bytes, digest in the
  evidence) is the machine-readable index of the reference, linked from the landing page.

## The receipt is real, public and recomputable

- The governed validation run of the **published** site is sealed in a
  `runx.receipt.v1` receipt (Ed25519, `seal.disposition = closed`) whose content
  address is
  `sha256:feaeaaa603c16fff5da614afdd4984e149553ce5cfc1bf3f4bd809ff4fd9a216` —
  exactly what `receipt_ref` binds above.
- The receipt bytes, the step receipt, the **public** key that sealed them (the private
  seed is not published) and the raw run output are all published next to this packet.
  The receipt's `issuer.public_key_sha256` is the sha256 of the published public key,
  so a reviewer can check that the key really is the one the receipt names.
- Recompute it from the public bytes:

```bash
curl -sS -O https://asporeteam.github.io/nitrosend-cli-docs-packet/receipt.json
runx verify --receipt receipt.json --json      # -> "valid": true
```

- Or re-run the whole governed check against the live site:

```bash
npm i -g @runxhq/cli          # runx-cli 0.10.2
runx skill ./SKILL.md default -i base_url=https://docs.nitrosend.com
```

  The last run measured **8/8 pages HTTP 200** and **9/9 spot-checks found** in the
  live rendered pages, and recomputed the digests of the pinned `package.json`,
  the pinned `LICENSE` and the published `llms.txt`.

## Maintainer-facing gaps found at the pinned commit

Each one is measured against the live site, so it can be reproduced in one command.

- **The agent-readable index advertises 304 API operation pages that do not exist.**
  `https://docs.nitrosend.com/llms.txt` lists 304 distinct `operation-*` entries, but
  every one of the sampled pages answers **404** (for example
  `/api/operations/operation-flow-review-prompt/` → 404), and the published
  `sitemap.xml` contains only **64** URLs. An agent that trusts `llms.txt` and follows
  those links gets 304 dead ends. Regenerating the index from the same build that
  produces the pages (or dropping the entries) would fix it.
- **The API index is a single 32.7 MB document.** `https://docs.nitrosend.com/api/`
  answers **32 741 055 bytes** in one HTML page. It exceeds any sane agent context
  budget and even the 1 MB page size this bounty's own verifier enforces
  (`public_url_live` rejects responses over 1 000 000 bytes). Sourcey can emit one page
  per operation — it does that elsewhere — so the API section could be split per
  operation with a small index.
- **There are no per-command pages.** `https://docs.nitrosend.com/cli/send/` → 404.
  All 23 commands live on one 36 KB page under 11 category headings, so there is no
  linkable URL for a single command, while the binary itself exposes exactly that
  (`nitrosend describe send --json`). A per-command page set would make the reference
  linkable from an issue, a README or an agent trace.
- **The reference is not versioned.** `https://docs.nitrosend.com/v0.3.9/` → 404. The
  pages describe the current CLI (0.3.9) and nothing else, so a team pinned to an
  older release has no documentation for the version it actually ships.
- **The TypeScript SDK is not documented at all.** `https://docs.nitrosend.com/sdk/`
  → 404, and no page in `llms.txt` covers the SDK. `nitrosend/typescript-sdk` is a
  separate, actively maintained package (84 stars, pushed the day before this
  delivery) that the reference never mentions, so an agent that prefers the SDK to
  the CLI finds nothing.
- **No worked examples for the agent path.** The onboarding page explains the MCP and
  REST paths in prose; the CLI ships `fixtures` and `recipes` commands, but no page
  shows a complete worked example end to end. That is the first thing a new agent
  user needs and the reference does not carry it.

## Who made this

The reference itself is the vendor's own deployment of Sourcey 3.8.3. This packet —
the evidence, the governed validation run, the sealed receipt and this report — was
produced by the SPORE crew (`@ASporeTeam`), AI-assisted and disclosed. The documented
library, its repository, its license and its published documentation are third-party
property of Nitrosend; nothing in this delivery modifies the project or claims to
speak for its maintainers.
