import sys
import json
import email
from email.utils import parsedate_tz, mktime_tz
from datetime import datetime

def parse_email_message():
    # Read raw email from stdin
    raw_email = sys.stdin.read()
    
    # Parse the email
    msg = email.message_from_string(raw_email)
    
    # Extract fields
    from_field = msg.get('From', '')
    to_field = msg.get('To', '')
    cc_field = msg.get('Cc', '')
    subject = msg.get('Subject', '')
    date_field = msg.get('Date', '')
    
    # Parse TO field into array
    to_list = []
    if to_field:
        to_list = [addr.strip() for addr in to_field.split(',')]
    
    # Parse CC field into array
    cc_list = []
    if cc_field:
        cc_list = [addr.strip() for addr in cc_field.split(',')]
    
    # Parse date to ISO format
    iso_date = ''
    if date_field:
        parsed_date = parsedate_tz(date_field)
        if parsed_date:
            timestamp = mktime_tz(parsed_date)
            dt = datetime.utcfromtimestamp(timestamp)
            iso_date = dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    # Extract body
    body = ''
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    
    # Check for attachments
    has_attachments = False
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                has_attachments = True
                break
    
    # Build result
    result = {
        'from': from_field,
        'to': to_list,
        'cc': cc_list,
        'subject': subject,
        'date': iso_date,
        'body': body.rstrip('\n') if body else '',
        'has_attachments': has_attachments
    }
    
    # Output JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == '__main__':
    parse_email_message()