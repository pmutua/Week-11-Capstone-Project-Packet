# Cost analysis

| Call type | Calls (n) | Unit cost | Total | Assumptions |
| --- | --- | --- | --- | --- |
| Stub tests (`pytest -q`) | 0 | $0 | $0 | No model call anywhere in the test path |
| Thursday demo (`curl` walkthrough) | 0 | $0 | $0 | `model_id` is `stub-local-router-v1`; this build has no live-model code path to call, so the demo is genuinely free, not merely capped |

This differs from the generic lesson template, which budgets ~$1 of live
calls for the Thursday demo. This capstone never wires a live model
provider, so there is nothing to bill -- see `docs/build_checkpoint.md`
for why that is a deliberate deferral, not an oversight.
