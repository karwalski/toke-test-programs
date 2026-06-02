import configparser
import os
import sys

def main():
    lines = sys.stdin.read().strip().split('\n')
    config_file = lines[0]
    
    # Initialize config parser
    config = configparser.ConfigParser()
    
    # Read existing config file if it exists
    if os.path.exists(config_file):
        config.read(config_file)
    
    # Process each command
    for i in range(1, len(lines)):
        command = lines[i].strip()
        if not command:
            continue
            
        parts = command.split(' ', 2)
        action = parts[0]
        
        if action == 'GET':
            section_key = parts[1]
            section, key = section_key.split('.', 1)
            
            if config.has_section(section) and config.has_option(section, key):
                print(config.get(section, key))
            else:
                print("KEY_NOT_FOUND")
                
        elif action == 'SET':
            section_key = parts[1]
            value = parts[2]
            section, key = section_key.split('.', 1)
            
            if not config.has_section(section):
                config.add_section(section)
            
            config.set(section, key, value)
            
            # Write to file
            with open(config_file, 'w') as f:
                config.write(f)
            
            print("OK")
            
        elif action == 'DEL':
            section_key = parts[1]
            section, key = section_key.split('.', 1)
            
            if config.has_section(section) and config.has_option(section, key):
                config.remove_option(section, key)
                
                # Remove section if it's empty
                if not config.options(section):
                    config.remove_section(section)
                
                # Write to file
                with open(config_file, 'w') as f:
                    config.write(f)
            
            print("OK")

if __name__ == "__main__":
    main()