# Sanitization note

Delivery path: no-deployment, representative data. No internal data, customer data or PII was used.

## Scan performed (2026-10-30, read-only)
- Key and token patterns in tracked files (sk-ant-, sk-or-, xoxb-, ghp_, github_pat_, AKIA, password=, secret=, api_key=): no real credential found.
- Credential files (google_cred.json, slack_token.txt, credentials.json, .env, .pem, id_rsa): none tracked; none ever committed in history.
- .gitignore covers .env, slack_token.txt, google_cred.json; credentials.json added.
- Local paths and personal email in tracked files: none.

## Known benign matches
- sk-ant-test-FAKEKEYDONOTUSE in docs/iteration-log-memory.md: a deliberately fake key from the Module 2 failure-mode test. It is not a real credential.
- Secret-pattern strings (sk-, password=) in CLAUDE.md, docs/memory-architecture.md and eval/test_policy.py: documentation of scanning rules, not secrets.
- xoxb-your-token in scripts/run-agent.sh: a placeholder default.
- scripts/run-reviewer.py reads ANTHROPIC_API_KEY from the environment by name only.

## Not covered
Commit author lines contain the author's GitHub email, which is already public on GitHub. No API key was registered for this project.
