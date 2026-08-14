---
name: asksecret
description: Create a one-time browser link for entering a secret without exposing its value in chat.
---

# Ask Secret

Create an opaque, one-time browser handoff for a secret value. The secret must
never be typed into the conversation, returned by an MCP tool, written to a
file, placed in an argument or environment variable, or included in a summary.

## Procedure

1. Read the optional user argument as the logical secret name. If absent, ask
   only how to name the secret; never ask for the secret value.
2. Confirm that the `AskSecret` MCP server exposes `get_secret`. If unavailable,
   report the capability unavailable and do not fall back to chat input.
3. Call `get_secret` with the name and a fresh opaque `request_id` when
   supported. Use registered-agent encryption; never use a base64/plaintext
   fallback.
4. When the result is missing or pending, show only the one-time `/i/<token>`
   browser URL as a clickable link.
5. Never display or forward a `/d/<token>` URL, blob path, bearer token, API
   key, or returned plaintext. Do not submit the form or fetch the secret.

Reply briefly that the user should open the one-time link and enter the value
there. A later approved consumer may retrieve it through the opaque runtime
path; the value must remain outside chat output.
