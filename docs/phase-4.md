# Phase 4 — Provider Gateway & Request-Side Optimization

Phase 4 adds the first provider-facing layer to V-Astra.

## Goal
Apply safe Phase 2/3 transformations to a provider request before the request
is handed to the provider SDK/transport.

## Provides
- Provider-agnostic `OptimizationGateway`.
- JSON request optimization for common `messages`/`input` payloads.
- Preservation of unknown fields.
- CLI command: `vastra provider`.
- Byte-level before/after optimization reporting.
- A sender callback for future Anthropic/Claude and other adapters.

## Safety boundary
This is a local wrapper/gateway, not an HTTPS man-in-the-middle proxy.
It does not decrypt arbitrary TLS traffic or claim transparent interception of
Claude Code network traffic. Credentials and transport remain with the caller.

## Example
`vastra provider request.json -o optimized-request.json --provider anthropic`

The original request is never modified in place.
