# Architecture

## Responsibility boundary

The application may collect inputs and display state. DidTheyAnswer owns the bounded on-chain record, authorization rules, semantic consensus call, and consequential state transition. There is no hidden backend or autonomous source collector.

## State machine

AWAITING_ANSWER -> READY_FOR_REVIEW -> FINAL, or READY_FOR_REVIEW -> CHALLENGE_OPEN -> READY_FOR_REVIEW -> FINAL.

## Storage model

The contract stores asker, respondent address text, question, criteria, answer, challenge, phase, verdict, round, and resolution. Text is normalized and field-length-bounded before storage.

## Consensus boundary

The leader serializes only stored case data into canonical JSON and requests an exact JSON schema. Validators independently run the same prompt and normalization path. A validator accepts only an allowed, structurally valid value that exactly matches its own result. Exceptions and malformed output fail closed.

## Authorization and invariants

The asker cannot answer. Only the asker can challenge or accept a nonfinal verdict. The first non-asker to submit becomes the respondent.

## Reuse and distinctness

Deploy one instance per question-and-respondent exchange. The instance preserves up to two review rounds and the challenge record.

This is a bounded conversational challenge protocol, not a contract dispute court or a one-shot answer label.
