import json
import sys

def render_dependency_tree(data):
    root_package = data["root_package"]
    dependencies = data["dependencies"]
    
    print(root_package)
    render_dependencies(dependencies, "", True)

def render_dependencies(deps, prefix, is_root):
    dep_items = list(deps.items())
    
    for i, (pkg_name, pkg_info) in enumerate(dep_items):
        is_last = (i == len(dep_items) - 1)
        
        if is_last:
            connector = "└── "
            next_prefix = prefix + "    "
        else:
            connector = "├── "
            next_prefix = prefix + "│   "
        
        version = pkg_info["version"]
        print(f"{prefix}{connector}{pkg_name}@{version}")
        
        if "dependencies" in pkg_info and pkg_info["dependencies"]:
            render_dependencies(pkg_info["dependencies"], next_prefix, False)

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read().strip())
    render_dependency_tree(input_data)