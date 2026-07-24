import argparse
import sys
import os
from scanner.core import scan_directory, scan_file
from agent.remediator import run_agentic_triage

def main():
    parser = argparse.ArgumentParser(description="Agentic Code Security Auditor")
    parser.add_argument("target", help="File or directory to scan")
    parser.add_argument("--no-agent", action="store_true", help="Disable the AI remediation layer and only show raw findings")
    
    args = parser.parse_args()
    
    target_path = args.target
    if not os.path.exists(target_path):
        print(f"Error: Target '{target_path}' does not exist.")
        sys.exit(1)
        
    print(f"🚀 Starting scan on: {target_path}")
    
    if os.path.isfile(target_path):
        findings = scan_file(target_path)
    else:
        findings = scan_directory(target_path)
        
    if not findings:
        print("✅ No vulnerabilities found. Great job!")
        sys.exit(0)
        
    if args.no_agent:
        print(f"\n🚨 Found {len(findings)} vulnerabilities (Agent disabled):\n")
        for f in findings:
            print(f"- {f['type']} at {f['file']}:{f['line']}")
            print(f"  {f['message']}\n")
        sys.exit(1) # Exit code 1 for pre-commit hooks to fail
        
    # Run the AI Triage
    run_agentic_triage(findings)
    sys.exit(1) # Return non-zero if issues were found to block commits

if __name__ == "__main__":
    main()
