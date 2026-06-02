import sys
import re

def strip_markdown(text):
    # Remove headers (# ## ### etc.)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove bold (**text** or __text__)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    # Remove italic (*text* or _text_)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Remove strikethrough (~~text~~)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    
    # Remove inline code (`text`)
    text = re.sub(r'`(.*?)`', r'\1', text)
    
    # Remove code blocks (