import json
import sys

# Read all input from stdin
input_data = sys.stdin.read().strip()

# Split by '---' to get current and proposed manifests
parts = input_data.split('---')
current_manifest = json.loads(parts[0].strip())
proposed_manifest = json.loads(parts[1].strip())

# Compare packages and find changes
for package in current_manifest:
    if package in proposed_manifest:
        current_version = current_manifest[package]
        proposed_version = proposed_manifest[package]
        if current_version != proposed_version:
            print(f"{package}: {current_version} -> {proposed_version}")