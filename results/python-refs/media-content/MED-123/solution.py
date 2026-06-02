import sys
import unicodedata
from collections import defaultdict

# Read input from stdin
text = sys.stdin.read().strip()

# Count characters by Unicode general category
category_counts = defaultdict(int)

for char in text:
    category = unicodedata.category(char)
    category_counts[category] += 1

# Map Unicode categories to simplified names
category_mapping = {
    'Lu': 'Letter',  # Letter, uppercase
    'Ll': 'Letter',  # Letter, lowercase
    'Lt': 'Letter',  # Letter, titlecase
    'Lm': 'Letter',  # Letter, modifier
    'Lo': 'Letter',  # Letter, other
    'Nd': 'DecimalDigit',  # Number, decimal digit
    'Nl': 'Number',  # Number, letter
    'No': 'Number',  # Number, other
    'Zs': 'Space',   # Separator, space
    'Zl': 'Space',   # Separator, line
    'Zp': 'Space',   # Separator, paragraph
    'Pc': 'Punctuation',  # Punctuation, connector
    'Pd': 'Punctuation',  # Punctuation, dash
    'Pe': 'Punctuation',  # Punctuation, close
    'Pf': 'Punctuation',  # Punctuation, final quote
    'Pi': 'Punctuation',  # Punctuation, initial quote
    'Po': 'Punctuation',  # Punctuation, other
    'Ps': 'Punctuation',  # Punctuation, open
    'Sm': 'Symbol',  # Symbol, math
    'Sc': 'Symbol',  # Symbol, currency
    'Sk': 'Symbol',  # Symbol, modifier
    'So': 'Symbol',  # Symbol, other
    'Mn': 'Mark',    # Mark, nonspacing
    'Mc': 'Mark',    # Mark, spacing combining
    'Me': 'Mark',    # Mark, enclosing
    'Cc': 'Control', # Other, control
    'Cf': 'Control', # Other, format
    'Cs': 'Control', # Other, surrogate
    'Co': 'Control', # Other, private use
    'Cn': 'Control'  # Other, not assigned
}

# Aggregate counts by simplified category names
simplified_counts = defaultdict(int)
for unicode_cat, count in category_counts.items():
    simplified_cat = category_mapping.get(unicode_cat, 'Other')
    simplified_counts[simplified_cat] += count

# Sort by count descending, then by category name for ties
sorted_categories = sorted(simplified_counts.items(), key=lambda x: (-x[1], x[0]))

# Output results
for category, count in sorted_categories:
    print(f"{category}: {count}")