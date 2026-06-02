import os
import sys
import time
import tempfile
import shutil
from pathlib import Path

class TempDirManager:
    def __init__(self):
        self.directories = {}
        self.base_path = "/tmp/managed"
        # Create base directory if it doesn't exist
        os.makedirs(self.base_path, exist_ok=True)
    
    def create(self, name, ttl_seconds):
        # Clean up expired directories first
        self._cleanup_expired()
        
        dir_path = os.path.join(self.base_path, name)
        os.makedirs(dir_path, exist_ok=True)
        
        created_at = time.time()
        self.directories[name] = {
            'path': dir_path,
            'created_at': created_at,
            'ttl': ttl_seconds
        }
        
        return dir_path
    
    def list_dirs(self):
        # Clean up expired directories first
        self._cleanup_expired()
        
        for name, info in self.directories.items():
            print(f"{name} {info['path']} {info['created_at']:.0f} {info['ttl']}")
    
    def cleanup(self):
        removed_count = 0
        current_time = time.time()
        
        to_remove = []
        for name, info in self.directories.items():
            if current_time - info['created_at'] >= info['ttl']:
                to_remove.append(name)
        
        for name in to_remove:
            info = self.directories[name]
            if os.path.exists(info['path']):
                shutil.rmtree(info['path'])
            del self.directories[name]
            removed_count += 1
        
        return removed_count
    
    def _cleanup_expired(self):
        current_time = time.time()
        to_remove = []
        
        for name, info in self.directories.items():
            if current_time - info['created_at'] >= info['ttl']:
                to_remove.append(name)
        
        for name in to_remove:
            info = self.directories[name]
            if os.path.exists(info['path']):
                shutil.rmtree(info['path'])
            del self.directories[name]

def main():
    manager = TempDirManager()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        command = parts[0]
        
        if command == "CREATE":
            name = parts[1]
            ttl_seconds = int(parts[2])
            dir_path = manager.create(name, ttl_seconds)
            print(dir_path)
        
        elif command == "LIST":
            manager.list_dirs()
        
        elif command == "CLEANUP":
            removed_count = manager.cleanup()
            print(f"Removed {removed_count} directories.")

if __name__ == "__main__":
    main()