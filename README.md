# Did They Answer

Provides a two-party question, answer, consensus review, challenge, and finalization workflow.

## Core workflow

- The asker stores a question and explicit answer criteria.
- A different address becomes the respondent by submitting the answer.
- Validators classify the answer as ANSWERED, PARTIAL, or EVADED.
- A non-answer opens an asker-only challenge or acceptance path; a second review is final.

## Reuse model

Deploy one instance per question-and-respondent exchange. The instance preserves up to two review rounds and the challenge record.

## Why GenLayer

Whether an answer substantively addresses a natural-language question under stated criteria cannot be reduced to exact string matching. GenLayer validators repeat the same bounded judgment before the verdict changes state.

## Evidence and source boundary

Only the stored question, criteria, respondent answer, and optional asker challenge are authoritative. No external fact-checking or source lookup occurs.

## Safety boundary

It judges responsiveness, not factual truth, expertise, completeness beyond the supplied criteria, or legal accountability. The contract holds no funds, has no upgrade hook, and never treats a model result as real-world certification.

## Verify locally

```text
python -m pip install -r requirements.txt
genvm-lint check contracts/did_they_answer.py
genvm-lint typecheck contracts/did_they_answer.py
pytest tests/direct -q
python tests/run_glsim.py --no-browser --seed 210821
gltest tests/integration/test_glsim_consensus.py -q --network localnet
```

Run the last two commands in separate terminals. Live StudioNet testing is opt-in and uses dedicated owner-specific keys outside this repository:

```text
gltest tests/integration/test_studionet_smoke.py -q -s --network studionet
```

Never commit a populated .env file, private key, keystore, or wallet password.

## Repository map

- contracts: deployable Intelligent Contract
- tests/direct: hardened state, authorization, malformed-output, and validator tests
- tests/integration: five-validator GLSim and live StudioNet flows
- deployments: public deployment and transaction evidence only
- SOURCE_POLICY.md: evidence authority and collection limits
- AUDIT.md: review-readiness checks and residual limitations
