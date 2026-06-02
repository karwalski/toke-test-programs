import configparser
import sys
import os

class PreservingConfigParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = []
        self.data = {}
        self._load()
    
    def _load(self):
        if not os.path.exists(self.filepath):
            return
        
        with open(self.filepath, 'r') as f:
            self.lines = f.readlines()
        
        # Parse the data
        current_section = None
        for line in self.lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#') or stripped.startswith(';'):
                continue
            if stripped.startswith('[') and stripped.endswith(']'):
                current_section = stripped[1:-1]
                if current_section not in self.data:
                    self.data[current_section] = {}
            elif '=' in stripped and current_section:
                key, value = stripped.split('=', 1)
                self.data[current_section][key.strip()] = value.strip()
    
    def get(self, section, key):
        if section in self.data and key in self.data[section]:
            return self.data[section][key]
        return None
    
    def set(self, section, key, value):
        if section not in self.data:
            self.data[section] = {}
        
        # Check if key exists and update in place
        section_found = False
        key_found = False
        
        for i, line in enumerate(self.lines):
            stripped = line.strip()
            if stripped == f'[{section}]':
                section_found = True
                continue
            elif stripped.startswith('[') and section_found:
                # We've moved to a different section, insert here
                self.lines.insert(i, f'{key}={value}\n')
                key_found = True
                break
            elif section_found and '=' in stripped:
                existing_key = stripped.split('=', 1)[0].strip()
                if existing_key == key:
                    self.lines[i] = f'{key}={value}\n'
                    key_found = True
                    break
        
        if not section_found:
            # Add new section
            if self.lines and not self.lines[-1].endswith('\n'):
                self.lines.append('\n')
            self.lines.append(f'[{section}]\n')
            self.lines.append(f'{key}={value}\n')
        elif not key_found:
            # Add key to existing section at the end
            self.lines.append(f'{key}={value}\n')
        
        self.data[section][key] = value
        self._save()
    
    def delete(self, section, key):
        if section not in self.data or key not in self.data[section]:
            return
        
        # Remove from data
        del self.data[section][key]
        
        # Remove from lines
        for i, line in enumerate(self.lines):
            stripped = line.strip()
            if '=' in stripped:
                existing_key = stripped.split('=', 1)[0].strip()
                if existing_key == key:
                    del self.lines[i]
                    break
        
        self._save()
    
    def sections(self):
        return list(self.data.keys())
    
    def _save(self):
        os.makedirs(os.path.dirname(self.filepath) if os.path.dirname(self.filepath) else '.', exist_ok=True)
        with open(self.filepath, 'w') as f:
            f.writelines(self.lines)

def main():
    filepath = input().strip()
    config = PreservingConfigParser(filepath)
    
    try:
        while True:
            line = input().strip()
            if not line:
                continue
            
            parts = line.split()
            command = parts[0]
            
            if command == "GET":
                section, key = parts[1], parts[2]
                value = config.get(section, key)
                if value is None:
                    print("KEY_NOT_FOUND")
                else:
                    print(value)
            
            elif command == "SET":
                section, key = parts[1], parts[2]
                value = ' '.join(parts[3:])
                config.set(section, key, value)
                print("OK")
            
            elif command == "DEL":
                section, key = parts[1], parts[2]
                config.delete(section, key)
                print("OK")
            
            elif command == "SECTIONS":
                sections = config.sections()
                print(' '.join(sections) if sections else '')
    
    except EOFError:
        pass

if __name__ == "__main__":
    main()