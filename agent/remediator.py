import sys
import json
import asyncio

try:
    from google.antigravity import Agent, LocalAgentConfig
except ImportError:
    # Fallback if SDK is not installed in the current environment
    print("WARNING: google.antigravity not installed. Using mock AI responses for MVP.")
    Agent = None

async def explain_and_fix(finding):
    """
    Takes a single finding dictionary from the scanner and uses an AI agent
    to explain the vulnerability and suggest a fix.
    """
    prompt = f"""
You are a Staff Security Engineer. Review the following code vulnerability:

Vulnerability Type: {finding['type']}
File: {finding['file']}
Line: {finding['line']}
Error Message: {finding['message']}

Code Snippet:
```python
{finding['snippet']}
```

Provide a brief, plain-English explanation of why this is dangerous, and output a secure replacement code block.
"""

    if Agent is None:
        return (
            "**Explanation (Mock)**: This vulnerability could allow an attacker to compromise the system.\n"
            "**Fix (Mock)**: Please replace the vulnerable pattern with a secure library function."
        )

    config = LocalAgentConfig(
        system_instructions="You are an expert security engineer providing clear explanations and secure code fixes."
    )
    
    try:
        async with Agent(config) as agent:
            # We would normally send the message and wait for the response text.
            # Assuming the agent object has a .chat() or similar method in antigravity SDK.
            # To keep this MVP generic, we mock the actual network call if the API changes.
            response = await agent.chat(prompt)
            return response.text
    except Exception as e:
        return f"Error contacting AI Agent: {e}"

def run_agentic_triage(findings):
    """
    Runs the agent over all findings and prints the results.
    """
    if not findings:
        print("✅ No vulnerabilities found. Your code is secure!")
        return

    print(f"🔍 Found {len(findings)} potential vulnerabilities. Running agentic triage...\n")
    
    async def triage_all():
        for i, finding in enumerate(findings, 1):
            print(f"[{i}/{len(findings)}] Analyzing {finding['type']} in {finding['file']}:{finding['line']}...")
            analysis = await explain_and_fix(finding)
            print("-" * 60)
            print(f"🚨 Finding: {finding['type']} ({finding['file']}:{finding['line']})")
            print(f"Message: {finding['message']}")
            print(f"Snippet:\n{finding['snippet']}")
            print("-" * 60)
            print(f"🤖 Agent Analysis:\n{analysis}\n")
            print("=" * 60 + "\n")

    asyncio.run(triage_all())

if __name__ == "__main__":
    # Test script with dummy finding
    dummy_finding = {
        'type': 'SQL_INJECTION',
        'file': 'tests/bad_code.py',
        'line': 12,
        'message': 'Potential SQL injection: string formatting/concatenation used inside execute().',
        'snippet': "query = f'SELECT * FROM users WHERE id = {user_id}'\ncursor.execute(query)"
    }
    asyncio.run(explain_and_fix(dummy_finding))
