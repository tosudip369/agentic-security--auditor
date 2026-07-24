# Agentic Code Security Auditor - SPEC

## 1. Overview
A lightweight, intelligent static-analysis security scanner. It parses source code to detect known vulnerabilities using deterministic AST traversal, and then layers an AI agent on top to explain the finding and suggest context-aware fixes. It acts like a mini open-source Snyk/CodeQL, supercharged with agentic intelligence.

## 2. Target Audience
Developers looking for an easy-to-install, immediate security feedback loop directly in their local workflow (via git hooks), preventing insecure code from ever making it to a remote branch.

## 3. Core Architecture
- **Language**: Python (chosen for excellent native AST parsing via the `ast` module and seamless AI SDK integration).
- **Scanner Core**: 
  - Scans target Python files.
  - Builds Abstract Syntax Trees (ASTs) using Python's built-in `ast` module.
  - Detects specific antipatterns via tree traversal:
    - Usage of `eval()` or `exec()`.
    - Hardcoded secrets (basic regex/entropy or variable name matching).
    - SQL injection risks (detecting string concatenation inside `.execute()` calls).
- **Agentic Layer**:
  - For each detected issue, an AI agent takes the raw code snippet and the vulnerability type.
  - Generates a plain-English explanation of *why* it's dangerous, plus a suggested secure replacement.
- **Git Hook Integration**:
  - A pre-commit hook script that automatically triggers the scanner on staged files.
- **Output**:
  - Terminal-based CLI report providing immediate, actionable feedback.

## 4. Implementation Phases (MVP)

**Phase 1: Foundation (Current)**
- [x] Repo initialization.
- [x] SPEC.md definition.
- [ ] Establish "agentic-devops-hub" style workflows (`.github/workflows`, `tasks/`).

**Phase 2: Core AST Scanner**
- [ ] Implement `scanner/core.py` using `ast.NodeVisitor`.
- [ ] Create rules for `eval` and basic hardcoded secrets.
- [ ] *Commit checkpoint.*

**Phase 3: Agent Layer Integration**
- [ ] Implement `agent/remediator.py` to process scanner output using an LLM API.
- [ ] *Commit checkpoint.*

**Phase 4: Git Hook & CLI Integration**
- [ ] Create `hooks/pre-commit` setup script.
- [ ] Polish CLI output (using `rich` or standard ANSI colors).
- [ ] *Commit checkpoint.*

**Phase 5: Polish & Documentation**
- [ ] Write `README.md` (with placeholder for demo GIF).
- [ ] Create `CONTRIBUTING.md`.
- [ ] Open initial GitHub issues for known limitations (e.g., adding JS/TS support).

## 5. Known Limitations (To be tracked as Issues)
- MVP only supports parsing Python (`.py`) files.
- Secret detection in MVP relies on simple variable name heuristics rather than deep entropy analysis.
