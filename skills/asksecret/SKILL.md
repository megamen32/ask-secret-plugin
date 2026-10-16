---
name: asksecret
description: Open a one-time browser form for a secret; generate its name automatically when omitted.
---

# Secret input form

Use for `/secret`, `/asksecret`, and requests to hand over a password or token.

1. Use the supplied name. If absent, call `ask_secret({})`; the server generates
   a name. If the loaded client schema still requires a name, generate
   `secret_<random UUID>` locally. Never ask the human to name it.
2. Call **AskSecret `ask_secret`**. It returns `pending` with `input_url`, or
   `ready`. Present only the actual `/i/<token>` URL as a clickable Markdown
   link: «Введите секрет в [защищённую форму](URL)».
3. Keep the returned name/request identity for retries and the authorized
   consumer. Reuse a pending form; do not create a series of different names.
4. Compatibility: if an older server's `ask_secret` says only "not ready" or
   is unavailable, call `get_secret` once with the SAME name. Forward only its
   `/i/` input link. For a transient transport error, reconnect/retry once with
   the same identity through the configured MCP; do not loop or alter credentials.
5. `ready` means already supplied. Do not request it again or fetch its value
   merely to show a form. An actual consumer needs the user's task authorization;
   use the existing encrypted stdin route (`ask_secret_run` / `sss-run`).

Never request plaintext in chat. Never show secret values, `/d/` download URLs,
encrypted blob paths or credentials. Never copy a secret into argv, environment,
logs, memory or a summary. Do not invent an input URL or claim a form exists
when the service returned no link. No automatic `.env` write merely from opening
this form. A missing input capability is an exact blocker, not a request to paste
secret values into chat.
