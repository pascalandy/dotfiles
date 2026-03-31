# WKWebView Limits

cmux browser runs inside WKWebView, so some browser-automation features are intentionally unavailable.

## Unsupported Capabilities

- Viewport emulation
- Offline emulation
- Trace or screencast recording
- Network interception or mocking
- Low-level raw input injection

## Safe Fallbacks

- Prefer `snapshot --interactive` plus `click`, `fill`, `type`, `select`, and `press`.
- Use `get url`, `get text body`, and `get html body` when rich snapshots fail.
- Use explicit waits for selector, text, URL, function, or load state.
