import json
import hashlib
import sys

# Read input
user_contacts = json.loads(input().strip())
server_hashes = json.loads(input().strip())

# Hash user contacts
user_hashes = []
contact_to_hash = {}
for contact in user_contacts:
    hash_value = "sha256_of_" + contact
    user_hashes.append(hash_value)
    contact_to_hash[hash_value] = contact

# Find matches
matched_contacts = []
unmatched_contacts = []

for contact in user_contacts:
    hash_value = "sha256_of_" + contact
    if hash_value in server_hashes:
        matched_contacts.append(contact)
    else:
        unmatched_contacts.append(contact)

# Output results
print("matched:", ", ".join(matched_contacts))
print("unmatched:", ", ".join(unmatched_contacts))
print("hashes_sent:", len(user_hashes))
print("hashes_compared:", len(user_hashes))