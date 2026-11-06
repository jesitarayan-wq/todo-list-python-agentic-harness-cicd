# Sanitization note

Sagaya Jesita Maria Sarath Raj · 2026-11-06

## Scope and result

No real credential was found in the tracked files, and no internal data, customer data or personal data was used. The delivery path is no-deployment, on representative data: a small to-do API.

## The scans of 2026-10-30 and 2026-11-06

The same four read-only checks were run on both dates. The second scan covered the revised repository (the branch `revision/final-alignment`, which has the same tracked files as `main` plus three document edits). Both found no real credential, no committed credential file and no personal paths.

| What was checked | Result |
| --- | --- |
| Key and token patterns in tracked files: `sk-ant-`, `sk-or-`, `xoxb-`, `ghp_`, `github_pat_`, `AKIA`, `password=`, `secret=`, `api_key=` | Only the known benign matches below |
| Credential files: `google_cred.json`, `slack_token.txt`, `credentials.json`, `.env`, `.pem`, `id_rsa` | None tracked, and none ever committed in history |
| `.gitignore` coverage | Covers `.env`, `slack_token.txt`, `google_cred.json` and `credentials.json` |
| Local paths and personal email in tracked files | None |

## Known benign matches

These matches look like secrets but are not.

| Match | Where | What it is |
| --- | --- | --- |
| `sk-ant-test-FAKEKEYDONOTUSE` | `docs/iteration-log-memory.md` | A deliberately fake key from the Module 2 failure-mode test; 27 characters; not a real credential |
| `password=test123` | `docs/iteration-log-memory.md` | A test value from the same memory-hook test |
| `API_KEY = "sk-demo-1234567890abcdef"` | `sample_review.py` | A deliberately fake value in the course's sample file, marked "Deliberate issue" |
| Secret-pattern strings (`sk-`, `password=`) | `CLAUDE.md`, `docs/memory-architecture.md`, `eval/test_policy.py` | Documentation of scanning rules, not secrets |
| `xoxb-your-token` | `scripts/run-agent.sh` | A placeholder default |
| `ANTHROPIC_API_KEY` | `scripts/run-reviewer.py` | Read from the environment by name only; no value is stored |

## Not covered

- Commit author lines contain the author's GitHub email, which is already public on GitHub.
- No API key was registered for this project.
- `.gitignore` has no `*.bak` rule (only `env.bak/` and `venv.bak/`). No `.bak` file is tracked, and files are added to commits by name, never with `git add .`.
- The scan reads tracked files only. `docs/live-run/live-run-session-2.txt` holds the full text of one agent session; it was searched for secret patterns on 2026-11-06 and showed no real match, and it should not be copied outside the repository.

## Still to do before resubmission

- Check that the re-recorded video shows no token, private page or inbox.
