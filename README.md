# Ask Secret Plugin

Portable [Agent Plugins 1.0](https://agent-plugins.org/specification) package
for requesting a secret through a one-time browser handoff. The secret value
never belongs in the agent conversation.

## Install

Point an Agent Plugins 1.0-compatible client at:

```text
https://github.com/megamen32/ask-secret-plugin
```

The plugin needs client-managed authorization for the configured AskSecret MCP
server. This repository contains no credentials.

## Use

Invoke the discovered `asksecret` skill or the client-specific `/asksecret`
command with an optional logical name, for example `github_token`. Without a
name the server generates one; the agent asks no naming questions. One
`ask_secret` call returns the input form. The user enters the value only at
the one-time browser URL; retrying the same pending request reuses the link.

## Source and safety

The source package is maintained in
[`megamen32/LastHumanCommit`](https://github.com/megamen32/LastHumanCommit).
CI validates the manifest, MCP configuration, skill boundaries, and secret-safe
package contents on every change and creates a GitHub release for `v*` tags.
