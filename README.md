# Frantic #33 delivery packet — Sourcey docs for nitrosend/cli

| artifact | URL |
|---|---|
| public_url (published docs, on the product's own domain) | https://docs.nitrosend.com/ |
| evidence_json | https://asporeteam.github.io/nitrosend-cli-docs-packet/evidence.json |
| report | https://asporeteam.github.io/nitrosend-cli-docs-packet/report.md |
| sealed runx receipt | https://asporeteam.github.io/nitrosend-cli-docs-packet/receipt.json |
| receipt public key (Ed25519; no private seed) | https://asporeteam.github.io/nitrosend-cli-docs-packet/receipt-public-key.json |
| step receipt | https://asporeteam.github.io/nitrosend-cli-docs-packet/receipt-step.json |
| governed run output | https://asporeteam.github.io/nitrosend-cli-docs-packet/verification-output.json |
| verifier | https://asporeteam.github.io/nitrosend-cli-docs-packet/verify-nitrosend.py |
| independent fact-check (script) | https://asporeteam.github.io/nitrosend-cli-docs-packet/fact-check.py |
| independent fact-check (result) | https://asporeteam.github.io/nitrosend-cli-docs-packet/fact-check.json |
| independent fact-check (summary) | https://asporeteam.github.io/nitrosend-cli-docs-packet/fact-check.md |

## Verify the receipt yourself

```sh
curl -sS -O https://asporeteam.github.io/nitrosend-cli-docs-packet/receipt.json
runx verify --receipt receipt.json --json     # -> "valid": true
```

## Re-run the governed check against the live site

```sh
npm i -g @runxhq/cli          # runx-cli 0.10.2
runx skill ./SKILL.md default -i base_url=https://docs.nitrosend.com
```

The documented library, its repository, its license and the published documentation are
third-party property of Nitrosend. The crew did not modify the upstream project; this
packet proves that the published reference is the Sourcey output of the pinned commit
and that the vendor itself builds, publishes and maintains it on its own domain.
