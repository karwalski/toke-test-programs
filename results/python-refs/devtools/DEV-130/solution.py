import sys
import os

def detect_language_from_extension(file_path):
    """Detect programming language based on file extension"""
    ext = os.path.splitext(file_path)[1].lower()
    
    language_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.go': 'Go',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.rs': 'Rust',
        '.kt': 'Kotlin',
        '.swift': 'Swift',
        '.scala': 'Scala',
        '.r': 'R',
        '.m': 'Objective-C',
        '.pl': 'Perl',
        '.sh': 'Shell',
        '.sql': 'SQL',
        '.html': 'HTML',
        '.css': 'CSS',
        '.jsx': 'JavaScript',
        '.tsx': 'TypeScript',
        '.vue': 'Vue',
        '.dart': 'Dart'
    }
    
    return language_map.get(ext)

def detect_language_from_filename(file_path):
    """Detect language/framework from specific filenames"""
    filename = os.path.basename(file_path).lower()
    
    if filename == 'package.json':
        return 'JavaScript'
    elif filename == 'requirements.txt':
        return 'Python'
    elif filename == 'gemfile':
        return 'Ruby'
    elif filename == 'composer.json':
        return 'PHP'
    elif filename == 'cargo.toml':
        return 'Rust'
    elif filename == 'go.mod':
        return 'Go'
    elif filename == 'pom.xml':
        return 'Java'
    elif filename == 'build.gradle':
        return 'Java'
    
    return None

def detect_infrastructure(file_path):
    """Detect infrastructure tools from filenames"""
    filename = os.path.basename(file_path).lower()
    infrastructure = []
    
    if filename == 'dockerfile' or filename.startswith('dockerfile.'):
        infrastructure.append('Docker')
    elif filename == 'docker-compose.yml' or filename == 'docker-compose.yaml':
        infrastructure.append('Docker')
    elif filename == 'vagrantfile':
        infrastructure.append('Vagrant')
    elif filename.endswith('.tf'):
        infrastructure.append('Terraform')
    elif filename == 'ansible.cfg' or filename.endswith('.yml') or filename.endswith('.yaml'):
        if 'ansible' in filename or 'playbook' in filename:
            infrastructure.append('Ansible')
    
    return infrastructure

def main():
    language_counts = {}
    infrastructure_set = set()
    total_files = 0
    
    # Read file paths from stdin
    for line in sys.stdin:
        file_path = line.strip()
        if not file_path:
            continue
            
        total_files += 1
        
        # Try to detect language from extension first
        language = detect_language_from_extension(file_path)
        
        # If no language detected from extension, try filename
        if not language:
            language = detect_language_from_filename(file_path)
        
        # Count languages
        if language:
            language_counts[language] = language_counts.get(language, 0) + 1
        
        # Detect infrastructure
        infra = detect_infrastructure(file_path)
        infrastructure_set.update(infra)
    
    # Generate report
    print("Technology Stack Report")
    print()
    
    # Languages section
    print("Languages:")
    if language_counts:
        for language in sorted(language_counts.keys()):
            count = language_counts[language]
            file_word = "file" if count == 1 else "files"
            print(f"  {language}: {count} {file_word}")
    print()
    
    # Infrastructure section
    print("Infrastructure:")
    if infrastructure_set:
        for infra in sorted(infrastructure_set):
            print(f"  {infra}: yes")
    print()
    
    # Total files
    print(f"Total files analysed: {total_files}")

if __name__ == "__main__":
    main()