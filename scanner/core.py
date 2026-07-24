import ast
import os

class SecurityNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.findings = []

    def visit_Call(self, node):
        # Detect eval()
        if isinstance(node.func, ast.Name) and node.func.id == 'eval':
            self.findings.append({
                'type': 'DANGEROUS_FUNCTION',
                'line': node.lineno,
                'message': 'Usage of dangerous function eval() detected. Can lead to Remote Code Execution (RCE).'
            })
        
        # Detect SQL injection risk (string formatting/concatenation inside .execute())
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
            if node.args:
                arg = node.args[0]
                is_risky = False
                if isinstance(arg, ast.JoinedStr): # f-string
                    is_risky = True
                elif isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute) and arg.func.attr == 'format':
                    is_risky = True
                elif isinstance(arg, ast.BinOp) and isinstance(arg.op, (ast.Add, ast.Mod)): # string concatenation or % formatting
                    is_risky = True
                    
                if is_risky:
                    self.findings.append({
                        'type': 'SQL_INJECTION',
                        'line': node.lineno,
                        'message': 'Potential SQL injection: string formatting/concatenation used inside execute(). Use parameterized queries instead.'
                    })

        self.generic_visit(node)

    def visit_Assign(self, node):
        # Detect hardcoded secrets
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id.lower()
                if any(kw in name for kw in ['secret', 'password', 'token', 'api_key']):
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        self.findings.append({
                            'type': 'HARDCODED_SECRET',
                            'line': node.lineno,
                            'message': f"Hardcoded secret detected in variable '{target.id}'. Never commit secrets to source code."
                        })
        self.generic_visit(node)

def scan_file(filepath):
    """Scans a single Python file for security vulnerabilities using AST."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)
        visitor = SecurityNodeVisitor()
        visitor.visit(tree)
        
        lines = source.splitlines()
        for finding in visitor.findings:
            finding['file'] = filepath
            # Extract the specific line and 1 line of context around it
            start = max(0, finding['line'] - 2)
            end = min(len(lines), finding['line'] + 1)
            finding['snippet'] = '\n'.join(lines[start:end])
            
        return visitor.findings
    except SyntaxError:
        print(f"Syntax error in {filepath}, skipping...")
        return []
    except Exception as e:
        print(f"Error scanning {filepath}: {e}")
        return []

def scan_directory(directory):
    """Recursively scans a directory for Python files."""
    all_findings = []
    for root, dirs, files in os.walk(directory):
        # Skip virtual environments and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('venv', 'env', '__pycache__')]
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                findings = scan_file(filepath)
                all_findings.extend(findings)
    return all_findings
