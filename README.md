# Agentic Code Security Auditor 🛡️🤖

A lightweight static-analysis security scanner that detects vulnerabilities using AST traversal and uses an AI agent to explain findings and suggest fixes.

![Demo](docs/demo-placeholder.gif) <!-- Placeholder for demo GIF showing the agent fixing a finding -->

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
