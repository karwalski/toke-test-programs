import os
import sys
import json
import shutil
from datetime import datetime

class TrashManager:
    def __init__(self):
        self.trash_dir = os.path.expanduser("~/.trash")
        self.metadata_file = os.path.join(self.trash_dir, ".metadata.json")
        self.ensure_trash_dir()
        
    def ensure_trash_dir(self):
        if not os.path.exists(self.trash_dir):
            os.makedirs(self.trash_dir)
            
    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_metadata(self, metadata):
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def trash_file(self, filepath):
        if not os.path.exists(filepath):
            return
            
        filename = os.path.basename(filepath)
        trash_path = os.path.join(self.trash_dir, filename)
        
        # Handle duplicate names by appending a number
        counter = 1
        original_trash_path = trash_path
        while os.path.exists(trash_path):
            name, ext = os.path.splitext(filename)
            trash_path = os.path.join(self.trash_dir, f"{name}_{counter}{ext}")
            counter += 1
        
        # Move file to trash
        shutil.move(filepath, trash_path)
        
        # Update metadata
        metadata = self.load_metadata()
        trash_filename = os.path.basename(trash_path)
        metadata[trash_filename] = {
            'original_path': os.path.abspath(filepath),
            'deleted_at': datetime.now().isoformat()
        }
        self.save_metadata(metadata)
        
        print(f"Moved to trash: {filename}")
    
    def list_trash(self):
        metadata = self.load_metadata()
        for filename, info in metadata.items():
            if os.path.exists(os.path.join(self.trash_dir, filename)):
                print(f"{filename} {info['original_path']} {info['deleted_at']}")
    
    def restore_file(self, name):
        metadata = self.load_metadata()
        
        # Find the file (handle case where name might not have the counter suffix)
        target_file = None
        for filename in metadata:
            if filename == name or filename.startswith(name.split('.')[0]):
                if os.path.exists(os.path.join(self.trash_dir, filename)):
                    target_file = filename
                    break
        
        if not target_file:
            return
            
        trash_path = os.path.join(self.trash_dir, target_file)
        original_path = metadata[target_file]['original_path']
        
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(original_path), exist_ok=True)
        
        # Move file back to original location
        shutil.move(trash_path, original_path)
        
        # Remove from metadata
        del metadata[target_file]
        self.save_metadata(metadata)
        
        print(f"Restored to {original_path}")
    
    def empty_trash(self):
        metadata = self.load_metadata()
        count = 0
        
        for filename in list(metadata.keys()):
            trash_path = os.path.join(self.trash_dir, filename)
            if os.path.exists(trash_path):
                os.remove(trash_path)
                count += 1
        
        # Clear metadata
        self.save_metadata({})
        
        print(f"Emptied {count} items")

def main():
    trash_manager = TrashManager()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' ', 1)
        command = parts[0]
        
        if command == "TRASH" and len(parts) == 2:
            filepath = parts[1]
            trash_manager.trash_file(filepath)
        elif command == "LIST":
            trash_manager.list_trash()
        elif command == "RESTORE" and len(parts) == 2:
            name = parts[1]
            trash_manager.restore_file(name)
        elif command == "EMPTY":
            trash_manager.empty_trash()

if __name__ == "__main__":
    main()