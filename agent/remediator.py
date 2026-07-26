import sys
import json
import asyncio
import os
import requests

# Load .env variables manually to avoid adding a python-dotenv dependency
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, val = line.strip().split('=', 1)
                os.environ[key] = val

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

    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        return (
            "**Error**: NVIDIA_API_KEY not found in environment or .env file.\n"
            "Please add it to a .env file to use the agentic remediation."
        )

    # NVIDIA NIM API configuration
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": "You are an expert security engineer providing clear explanations and secure code fixes."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.2
    }

    try:
        # We use requests running synchronously since this is just an MVP CLI tool
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error contacting AI Agent via NVIDIA API: {e}"
    except (KeyError, IndexError) as e:
        return f"Error parsing AI response: {e}"

def run_agentic_triage(findings):
    """
    Runs the agent over all findings and prints the results.
    """
    if not findings:
        print("✅ No vulnerabilities found. Your code is secure!")
        return

    print(f"🔍 Found {len(findings)} potential vulnerabilities. Running agentic triage via NVIDIA API...\n")
    
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
    dummy_finding = {
        'type': 'SQL_INJECTION',
        'file': 'tests/bad_code.py',
        'line': 12,
        'message': 'Potential SQL injection: string formatting/concatenation used inside execute().',
        'snippet': "query = f'SELECT * FROM users WHERE id = {user_id}'\\ncursor.execute(query)"
    }
    asyncio.run(explain_and_fix(dummy_finding))

