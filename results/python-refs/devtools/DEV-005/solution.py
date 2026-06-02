import sys
from collections import defaultdict

def main():
    # Dictionary to store author statistics
    author_stats = defaultdict(lambda: {
        'commits': 0,
        'files_changed': 0,
        'insertions': 0,
        'deletions': 0
    })
    
    # Read from stdin and process each line
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        # Parse the pipe-separated values
        parts = line.split('|')
        if len(parts) != 5:
            continue
            
        author = parts[0]
        # date = parts[1]  # Not needed for output
        files_changed = int(parts[2])
        insertions = int(parts[3])
        deletions = int(parts[4])
        
        # Update author statistics
        author_stats[author]['commits'] += 1
        author_stats[author]['files_changed'] += files_changed
        author_stats[author]['insertions'] += insertions
        author_stats[author]['deletions'] += deletions
    
    # Sort authors by commits in descending order
    sorted_authors = sorted(author_stats.items(), 
                          key=lambda x: x[1]['commits'], 
                          reverse=True)
    
    # Output the results
    for author, stats in sorted_authors:
        print(f"{author}: {stats['commits']} commits, {stats['files_changed']} files, +{stats['insertions']} -{stats['deletions']}")

if __name__ == "__main__":
    main()