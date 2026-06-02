import sys
import re

def parse_unified_diff():
    lines = sys.stdin.read().strip().split('\n')
    files = {}
    current_file = None
    
    for line in lines:
        # Match file headers
        if line.startswith('--- '):
            continue
        elif line.startswith('+++ '):
            # Extract filename from +++ b/filename
            match = re.match(r'\+\+\+ b/(.+)', line)
            if match:
                current_file = match.group(1)
                files[current_file] = {'additions': 0, 'deletions': 0}
        elif line.startswith('@@'):
            continue
        elif current_file and line.startswith('+'):
            files[current_file]['additions'] += 1
        elif current_file and line.startswith('-'):
            files[current_file]['deletions'] += 1
    
    return files

def format_output(files):
    total_files = len(files)
    total_additions = sum(f['additions'] for f in files.values())
    total_deletions = sum(f['deletions'] for f in files.values())
    
    # Print per-file stats
    for filename, stats in files.items():
        print(f"{filename} | +{stats['additions']} -{stats['deletions']}")
    
    # Print summary
    file_word = "file" if total_files == 1 else "files"
    insertion_word = "insertion" if total_additions == 1 else "insertions"
    deletion_word = "deletion" if total_deletions == 1 else "deletions"
    
    print(f"{total_files} {file_word} changed, {total_additions} {insertion_word}(+), {total_deletions} {deletion_word}(-)")

if __name__ == "__main__":
    files = parse_unified_diff()
    format_output(files)