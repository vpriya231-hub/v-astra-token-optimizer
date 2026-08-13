# Claude Code Input Optimization

V-Astra's Claude profile is designed around the main input surfaces seen in coding-agent sessions:

- tool catalogs
- repeated tool results
- terminal/log output
- file context
- diffs and errors
- repeated history/context blocks

Phase 3 exposes the transformations as local primitives. Automatic Claude Code traffic interception is intentionally deferred to Phase 4 so that the proxy can be tested independently and fail-open.

## Planned Phase 4 path

```text
Claude Code
    ↓
V-Astra local proxy
    ↓
classify request payload
    ↓
shrink tool catalog / dedupe context / compress tool results
    ↓
recovery store
    ↓
Anthropic provider
```
