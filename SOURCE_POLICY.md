# Evidence and Source Policy

## Authoritative evidence

Only the stored question, criteria, respondent answer, and optional asker challenge are authoritative. No external fact-checking or source lookup occurs.

## Collection and provenance

Deployers and callers must collect text lawfully, verify provenance when it matters, and remove secrets or unnecessary personal data. On-chain storage proves which text was evaluated, not who authored it or whether it is true.

## Source selection and freshness

The contract performs no web request, search, browsing, API lookup, or hidden source selection. It makes no live-data or freshness claim. When facts or policies change, use the contract's documented update path or deploy a new appropriate instance.

## Prompt-injection and output controls

Caller text is untrusted data. It is canonicalized into a delimited payload; the prompt forbids treating embedded text as instructions. Only the documented strict JSON shape and closed values can pass normalization and validator replay.

## Production boundary

It judges responsiveness, not factual truth, expertise, completeness beyond the supplied criteria, or legal accountability. Higher-stakes applications need independent provenance, identity, privacy, appeal, and human-review processes proportionate to risk.
