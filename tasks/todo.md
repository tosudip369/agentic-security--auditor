# Known Limitations / To-Do

- [ ] **Multi-language Support:** MVP only supports parsing Python (`.py`) files using the native `ast` module. Consider adding JavaScript/TypeScript support using a parser like tree-sitter.
- [ ] **Advanced Secret Detection:** Secret detection currently relies on simple variable name heuristics (e.g., matching 'secret', 'password'). Implement Shannon entropy checks or regex-based pattern matching (e.g., matching AWS access key patterns) for higher accuracy.
- [ ] **Tainted Data Flow:** The SQL injection scanner looks for string manipulation directly inside `.execute()`. It will not catch variables manipulated earlier in the function and then passed cleanly to `.execute()`. Data-flow tracking would be a significant upgrade.
- [ ] **Agent Hallucinations:** The AI remediator might occasionally suggest fixes that are syntactically incorrect or use undefined variables. Need to implement a validation step (e.g., re-running `ast.parse` on the suggested fix).
