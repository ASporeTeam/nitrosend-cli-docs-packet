---
name: nitrosend-docs-verify
description: Re-verify the published Sourcey documentation site for nitrosend/cli at the pinned commit, and record the checks in a sealed runx receipt.
---

# Verify the published Sourcey site for Nitrosend

This skill is the governed validation run for the Frantic bounty
"Publish Sourcey docs for a maintained OSS library" (bounty #33).

It re-fetches the **published** documentation site on the project's own
registered domain, checks that every page a reviewer would open answers 200,
spot-checks the documented MCP surface against the rendered pages, and
recomputes the digests of the upstream Sourcey config and the LICENSE file at
the pinned commit. Everything it prints is a fact it measured during the run,
and the run itself is sealed into a `runx.receipt.v1` receipt.

The skill performs no writes to the published site and spends nothing.
