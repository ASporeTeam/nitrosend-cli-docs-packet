# Independent fact-check of this packet

Measured 2026-10-22T12:53:34Z by `fact-check.py` (published next to this file). **42/42 checks PASS, 0 FAIL.** GET-only: no venue write, no spend.

| what | measured |
|---|---|
| public_url | https://docs.nitrosend.com/ |
| receipt_ref | `runx:receipt:sha256:feaeaaa603c16fff5da614afdd4984e149553ce5cfc1bf3f4bd809ff4fd9a216` |
| documented pages answering 200 | 7/7 (+ /llms.txt = 8) |
| pages carrying the Sourcey generator tag | 7/7 |
| llms.txt | 131904 bytes, sha256 `19a451ea3a19c295f9ae44b791c75350c9255d198c7ae1e3ad405133d1df2eab` |
| llms.txt links | 585 (464 under /api/, 303 linked operation pages, 304 distinct operation names) |
| sitemap.xml URLs | 64 |
| /api/ index page | 32742055 bytes |
| CLI commands documented | 23 |
| CLI flags documented | 53 (usage blocks) |
| CLI category headings on one page | 11 |
| github.com/nitrosend/cli | 88 stars, 2 forks, pushed 2026-10-21T09:58:36Z |

## Vendor pipeline (first-party)

| field | value |
|---|---|
| repo | https://github.com/nitrosend/docs |
| sourcey.config.ts sha256 | `3384861c7912534502232ebc5325dea389cd82494bd6507cf9c334ade3269193` |
| package.json sha256 | `52517f1dff4b5c5f708ed6ba84985c056b78d16f8ac1ec28992413177d7ef72e` |
| siteUrl | https://docs.nitrosend.com |
| sourcey version | ^3.8.3 |
| CLI dev dependency | 0.3.9 |
| prebuild | `node scripts/check-plan-shape-content.mjs && node scripts/generate-cli-reference.mjs` |

## Every check

| status | id | measured |
|---|---|---|
| PASS | packet.evidence.json | 200 |
| PASS | packet.report.md | 200 |
| PASS | packet.receipt.json | 200 |
| PASS | packet.receipt-public-key.json | 200 |
| PASS | packet.receipt-step.json | 200 |
| PASS | packet.verification-output.json | 200 |
| PASS | packet.README.md | 200 |
| PASS | packet.verify-nitrosend.py | 200 |
| PASS | receipt.ref_matches_receipt_id | runx:receipt:sha256:feaeaaa603c16fff5da614afdd4984e149553ce5cfc1bf3f4bd809ff4fd9a216 |
| PASS | receipt.digest | sha256:6adc9686a2ff559ad |
| PASS | receipt.pubkey_matches_issuer | sha256:eec8d1a43965434999916279ffe6c27ff4e7270a0664eee9c6b8546c5d00f9a0 |
| PASS | receipt.pubkey_is_not_the_seed | no seed |
| PASS | receipt.runx_verify | True |
| PASS | upstream.cli_facts | archived=False license=MIT lang=TypeScript |
| PASS | upstream.pinned_commit | 1780c3f3 2026-10-21 chore(release): 0.3.9 |
| PASS | vendor.pipeline_siteurl | present |
| PASS | vendor.sourcey_version | ^3.8.3 |
| PASS | vendor.cli_version | 0.3.9 |
| PASS | vendor.openapi_adapter | present |
| PASS | site.documented_pages_200 | 7 of 7 |
| PASS | site.generator_tag | 7 of 7 |
| PASS | site.llms_digest | 19a451ea3a19c295f9ae44b791c75350c9255d198c7ae1e3ad405133d1df2eab |
| PASS | site.llms_size | 131904 |
| PASS | site.sitemap_urls | 64 |
| PASS | site.api_index_size | 32742055 |
| PASS | site.gap_cli_send | 404 |
| PASS | site.gap_v0.3.9 | 404 |
| PASS | site.gap_sdk | 404 |
| PASS | site.command_count | 23 |
| PASS | site.category_headings | 11 |
| PASS | site.flag_count | 53 |
| PASS | report.stars_forks | github now: 88 stars / 2 forks |
| PASS | report.no_bogus_forks | no '94 forks' |
| PASS | report.api_bytes | measured 32742055 |
| PASS | report.api_link_count | measured 464 |
| PASS | report.operation_counts | measured 303 links / 304 tokens |
| PASS | report.llms_bytes | measured 131904 |
| PASS | report.sitemap_urls | measured 64 |
| PASS | report.vendor_pipeline | mentions github.com/nitrosend/docs |
| PASS | report.receipt_ref | sha256:feaeaaa603c16fff5da614afdd4984e149553ce5cfc1bf3f4bd809ff4fd9a216 |
| PASS | report.command_count | measured 23 |
| PASS | report.flag_count | measured 53 |

## What this check repaired

The first published version of `report.md` carried four numbers that did not survive
re-measurement: the star/fork counts of the target repository, the byte size of
`/api/`, the number of operation pages listed in `llms.txt`, and the number of
documented CLI flags. All four were corrected in `report.md` at 12:50Z (in the
direction of the measured truth - the documented surface is larger than first
claimed, not smaller). `evidence.json`, the sealed receipt, the public key and the
governed run output were left byte-identical, so the machine-verified snapshot and
the live bytes still agree.

