import sys
import json

def mask_email(email):
    if '@' in email:
        local, domain = email.split('@', 1)
        if len(local) > 1:
            masked_local = local[0] + '***'
        else:
            masked_local = '***'
        return f"{masked_local}@{domain}"
    return email

def mask_phone(phone):
    # Find the last dash and keep everything after it
    if '-' in phone:
        parts = phone.split('-')
        masked_parts = ['***'] * (len(parts) - 1) + [parts[-1]]
        return '-'.join(masked_parts)
    else:
        # If no dash, mask most of it but keep last few digits
        if len(phone) > 4:
            return '***' + phone[-4:]
        else:
            return '***'

def mask_ssn(ssn):
    # SSN format is typically XXX-XX-XXXX, mask to ***-**-XXXX
    if '-' in ssn:
        parts = ssn.split('-')
        if len(parts) == 3:
            return f"***-**-{parts[2]}"
    # If no dashes, assume 9 digits and mask first 5
    if len(ssn) >= 4:
        return '***' + ssn[-4:]
    return '***'

def mask_credit_card(cc):
    # Remove any spaces or dashes first
    digits_only = ''.join(c for c in cc if c.isdigit())
    if len(digits_only) >= 4:
        return '****-****-****-' + digits_only[-4:]
    return '****'

def mask_field(field_name, value):
    if not isinstance(value, str):
        return value
    
    if field_name == 'email':
        return mask_email(value)
    elif field_name == 'phone':
        return mask_phone(value)
    elif field_name == 'ssn':
        return mask_ssn(value)
    elif field_name == 'credit_card' or field_name == 'creditcard':
        return mask_credit_card(value)
    else:
        return value

def main():
    lines = sys.stdin.read().strip().split('\n')
    
    # First line contains fields to mask
    fields_to_mask = set(lines[0].split())
    
    # Process each JSON object
    for i in range(1, len(lines)):
        if lines[i].strip():
            try:
                json_obj = json.loads(lines[i])
                
                # Mask specified fields
                for field_name in fields_to_mask:
                    if field_name in json_obj:
                        json_obj[field_name] = mask_field(field_name, json_obj[field_name])
                
                # Output JSON with no extra spaces
                print(json.dumps(json_obj, separators=(',', ':')))
                
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    main()