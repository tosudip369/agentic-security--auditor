import os
import stat
import sys

HOOK_CONTENT = """#!/usr/bin/env bash
# Agentic Security Pre-commit Hook

echo "🛡️  Running Agentic Security Auditor on staged files..."

# Get all staged Python files
staged_files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' || true)

if [ -z "$staged_files" ]; then
    exit 0
fi

has_errors=0

for file in $staged_files; do
    echo "Scanning $file..."
    # Run the scanner without the agent (just fast AST check) for the hook
    python main.py "$file" --no-agent
    if [ $? -ne 0 ]; then
        has_errors=1
    fi
done

if [ $has_errors -ne 0 ]; then
    echo "❌ Security vulnerabilities found! Please fix them before committing."
    echo "   To see AI remediation suggestions, run: python main.py <file>"
    exit 1
fi

echo "✅ Security checks passed."
exit 0
"""

def install_hook():
    git_dir = os.path.join('.git', 'hooks')
    if not os.path.exists(git_dir):
        print("Error: .git/hooks directory not found. Are you in the repository root?")
        sys.exit(1)
        
    hook_path = os.path.join(git_dir, 'pre-commit')
    
    with open(hook_path, 'w', newline='\n') as f:
        f.write(HOOK_CONTENT)
        
    # Make executable on Unix/Mac (not strictly required on Windows but good practice)
    try:
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
    except Exception:
        pass
        
    print(f"✅ Successfully installed pre-commit hook at {hook_path}")

if __name__ == "__main__":
    install_hook()
