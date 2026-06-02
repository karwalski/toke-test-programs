import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    books = json.loads(input_data)
    
    total_books = 0
    total_pages = 0
    total_days = 0
    longest_book = None
    max_pages = 0
    
    # Process each book
    for book in books:
        title = book["title"]
        pages = book["pages"]
        start_date = datetime.strptime(book["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(book["end_date"], "%Y-%m-%d")
        
        # Calculate days (inclusive)
        days = (end_date - start_date).days + 1
        
        # Print log entry
        print(f"{title}: {pages} pages ({days} days)")
        
        # Update statistics
        total_books += 1
        total_pages += pages
        total_days += days
        
        # Track longest book
        if pages > max_pages:
            max_pages = pages
            longest_book = title
    
    # Calculate average pages per day
    avg_pages_per_day = total_pages / total_days
    
    # Print statistics
    print(f"Total books: {total_books}")
    print(f"Total pages: {total_pages}")
    print(f"Avg pages/day: {avg_pages_per_day}")
    print(f"Longest book: {longest_book}")

if __name__ == "__main__":
    main()