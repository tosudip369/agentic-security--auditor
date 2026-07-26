![Version](https://img.shields.io/badge/version-v1.1.0-blue.svg)
# Agentic Code Security Auditor 🛡️🤖

A lightweight static-analysis security scanner that detects vulnerabilities using AST traversal and uses an AI agent to explain findings and suggest fixes.

Here is what it looks like when the agentic triage runs on vulnerable code:

```text
🚀 Starting scan on: bad_code.py
🔍 Found 2 potential vulnerabilities. Running agentic triage...

[1/2] Analyzing DANGEROUS_FUNCTION in bad_code.py:8...
------------------------------------------------------------
🚨 Finding: DANGEROUS_FUNCTION (bad_code.py:8)
Message: Usage of dangerous function eval() detected. Can lead to Remote Code Execution (RCE).
Snippet:
user_input = "os.system('rm -rf /')"
eval(user_input)
------------------------------------------------------------
🤖 Agent Analysis:
This is highly dangerous because `eval()` executes arbitrary strings as Python code. If `user_input` comes from an untrusted source, an attacker could run malicious commands like deleting files (RCE).

**Secure Fix:** 
Use `ast.literal_eval()` if you only need to evaluate safe Python literals, or redesign the logic to avoid dynamic code execution entirely.

============================================================

[2/2] Analyzing HARDCODED_SECRET in bad_code.py:11...
------------------------------------------------------------
🚨 Finding: HARDCODED_SECRET (bad_code.py:11)
Message: Hardcoded secret detected in variable 'api_secret'. Never commit secrets to source code.
Snippet:
# Bad practice: hardcoded secret
api_secret = "AKIAIOSFODNN7EXAMPLE"
------------------------------------------------------------
🤖 Agent Analysis:
Committing secrets to source control means anyone with read access to the repo can steal and misuse them. 

**Secure Fix:** 
Load secrets from environment variables or a secure vault.
```python
import os
api_secret = os.environ.get("API_SECRET")
```
============================================================
```

## Features
- **AST-Based Scanner**: Deterministic pattern matching for `eval()`, SQL Injections, and Hardcoded Secrets without relying on LLM guesswork.
- **Agentic Remediation**: Uses the Antigravity AI SDK to read flagged snippets and provide plain-English explanations and secure refactors.
- **Pre-commit Hooks**: Stop vulnerable code before it ever reaches a remote branch.

## Quickstart

1. **Install the Pre-Commit Hook:**
   ```bash
   python setup_hooks.py
   ```
   Now, every time you `git commit`, the fast AST scanner will check your staged files.

2. **Run Manual Triage (with AI):**
   ```bash
   python main.py path/to/your/file.py
   ```
   This runs the scanner and streams the findings to the AI agent for detailed remediation.

3. **Run Fast Scan (without AI):**
   ```bash
   python main.py path/to/your/file.py --no-agent
   ```

## Architecture
This project is built to demonstrate engineering first, AI second. 
The core engine (`scanner/core.py`) is written using Python's native `ast` module to ensure strict, deterministic detection of antipatterns. The LLM is strictly positioned as a presentation and remediation layer (`agent/remediator.py`).

