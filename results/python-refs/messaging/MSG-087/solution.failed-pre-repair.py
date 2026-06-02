import json
import sys

def parse_command_line(line):
    """Parse a command line into tokens, respecting quoted strings."""
    tokens = []
    current_token = ""
    in_quotes = False
    quote_char = None
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if not in_quotes:
            if char in ['"', "'"]:
                in_quotes = True
                quote_char = char
            elif char == ' ':
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char
        else:
            if char == quote_char:
                in_quotes = False
                quote_char = None
            else:
                current_token += char
        
        i += 1
    
    if current_token:
        tokens.append(current_token)
    
    return tokens

def parse_message(message, command_registry):
    """Parse a message and return the appropriate output."""
    message = message.strip()
    
    # Check if it's a command (starts with /)
    if not message.startswith('/'):
        return "NOT_A_COMMAND"
    
    # Parse the command line
    tokens = parse_command_line(message[1:])  # Remove the leading /
    
    if not tokens:
        return "NOT_A_COMMAND"
    
    command_name = tokens[0]
    
    # Find the command in the registry
    command_def = None
    for cmd in command_registry:
        if cmd['name'] == command_name:
            command_def = cmd
            break
    
    if command_def is None:
        return f'ERROR: unknown command "{command_name}"'
    
    # Parse arguments and flags
    args = {}
    flags = []
    arg_tokens = tokens[1:]
    
    # Separate flags from arguments
    non_flag_tokens = []
    i = 0
    while i < len(arg_tokens):
        token = arg_tokens[i]
        if token.startswith('--') and token in command_def['flags']:
            flags.append(token)
        else:
            non_flag_tokens.append(token)
        i += 1
    
    # Match positional arguments
    required_args = [arg for arg in command_def['args'] if arg['required']]
    
    # Check if we have enough arguments
    if len(non_flag_tokens) < len(required_args):
        return f'ERROR: missing required arguments'
    
    # Assign arguments
    for i, arg_def in enumerate(command_def['args']):
        if i < len(non_flag_tokens):
            args[arg_def['name']] = non_flag_tokens[i]
        elif arg_def['required']:
            return f'ERROR: missing required argument "{arg_def["name"]}"'
    
    # Format output
    args_str = ", ".join([f'{k}: "{v}"' for k, v in args.items()])
    flags_str = ", ".join(flags)
    
    result = f"COMMAND: {command_name}, args: {{{args_str}}}, flags: [{flags_str}]"
    return result

def main():
    # Read the command registry
    registry_line = input().strip()
    command_registry = json.loads(registry_line)
    
    # Process each message
    try:
        while True:
            message = input()
            result = parse_message(message, command_registry)
            print(result)
    except EOFError:
        pass

if __name__ == "__main__":
    main()