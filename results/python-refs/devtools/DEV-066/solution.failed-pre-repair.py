import sys
import ast
import os

def analyze_python_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        # Track assigned variables and their line numbers
        assigned_vars = {}  # name -> line_number
        used_vars = set()
        
        class VariableAnalyzer(ast.NodeVisitor):
            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_vars[target.id] = node.lineno
                self.generic_visit(node)
            
            def visit_AugAssign(self, node):
                if isinstance(node.target, ast.Name):
                    assigned_vars[node.target.id] = node.lineno
                self.generic_visit(node)
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    used_vars.add(node.id)
                self.generic_visit(node)
            
            def visit_FunctionDef(self, node):
                # Function parameters are considered used
                for arg in node.args.args:
                    used_vars.add(arg.arg)
                self.generic_visit(node)
            
            def visit_For(self, node):
                # For loop variables are considered used
                if isinstance(node.target, ast.Name):
                    used_vars.add(node.target.id)
                self.generic_visit(node)
            
            def visit_comprehension(self, node):
                if isinstance(node.target, ast.Name):
                    used_vars.add(node.target.id)
                self.generic_visit(node)
        
        analyzer = VariableAnalyzer()
        analyzer.visit(tree)
        
        # Find unused variables
        unused = []
        for var_name, line_num in assigned_vars.items():
            if var_name not in used_vars and not var_name.startswith('_'):
                unused.append((line_num, var_name))
        
        return sorted(unused)
    
    except Exception:
        return []

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        return
    
    language = lines[0]
    
    if language != 'python':
        return
    
    for filepath in lines[1:]:
        if os.path.exists(filepath):
            unused_vars = analyze_python_file(filepath)
            for line_num, var_name in unused_vars:
                print(f"{filepath}:{line_num}: unused variable: {var_name}")

if __name__ == "__main__":
    main()