import json
import sys

def parse_command_line(line):
    tokens = []
    current_token = ""
    in_quotes = False
    quote_char = None
    has_token = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if not in_quotes:
            if char in ['"', "'"]:
                in_quotes = True
                quote_char = char
                has_token = True
            elif char == ' ':
                if has_token:
                    tokens.append(current_token)
                    current_token = ""
                    has_token = False
            else:
                current_token += char
                has_token = True
        else:
            if char == quote_char:
                in_quotes = False
                quote_char = None
            else:
                current_token += char
        
        i += 1
    
    if has_token:
        tokens.append(current_token)
    
    return tokens

def parse_message(message, command_registry):
    message = message.strip()
    
    if not message.startswith('/'):
        return "NOT_A_COMMAND"
    
    tokens = parse_command_line(message[1:])
    
    if not tokens:
        return "NOT_A_COMMAND"
    
    command_name = tokens[0]
    
    command_def = None
    for cmd in command_registry:
        if cmd['name'] == command_name:
            command_def = cmd
            break
    
    if command_def is None:
        return f'ERROR: unknown command "{command_name}"'
    
    args = {}
    flags = []
    arg_tokens = tokens[1:]
    
    non_flag_tokens = []
    quoted_positions = set()
    
    # Re-parse to track which tokens were quoted
    # Simpler: just check if token starts with -- and is in flags
    for token in arg_tokens:
        if token.startswith('--') and token in command_def['flags']:
            flags.append(token)
        else:
            non_flag_tokens.append(token)
    
    expected_arg_count = len(command_def['args'])
    
    # Check arg count
    required_count = len([a for a in command_def['args'] if a['required']])
    
    if len(non_flag_tokens) > expected_arg_count:
        # Need to merge extra tokens into the last argument
        if expected_arg_count > 0:
            # Merge extras into last arg
            merged = non_flag_tokens[:expected_arg_count-1] + [' '.join(non_flag_tokens[expected_arg_count-1:])]
            non_flag_tokens = merged
        else:
            return f'ERROR: "{command_name}" takes 0 arguments, got {len(non_flag_tokens)}'
    
    if len(non_flag_tokens) < required_count:
        return f'ERROR: missing required arguments'
    
    for i, arg_def in enumerate(command_def['args']):
        if i < len(non_flag_tokens):
            args[arg_def['name']] = non_flag_tokens[i]
        elif arg_def['required']:
            return f'ERROR: missing required argument "{arg_def["name"]}"'
    
    args_str = ", ".join([f'{k}: "{v}"' for k, v in args.items()])
    flags_str = ", ".join(flags)
    
    return f"COMMAND: {command_name}, args: {{{args_str}}}, flags: [{flags_str}]"

def main():
    registry_line = input().strip()
    command_registry = json.loads(registry_line)
    
    try:
        while True:
            message = input()
            result = parse_message(message, command_registry)
            print(result)
    except EOFError:
        pass

if __name__ == "__main__":
    main()