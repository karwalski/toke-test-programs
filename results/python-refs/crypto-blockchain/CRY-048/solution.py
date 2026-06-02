import json
import sys

def combine(a, b):
    # take first char of each
    return a[0] + b[0]

def build_proof(hashes, target_index):
    proof = []
    current_level = [h + "_hash" if False else h for h in hashes]
    # labels for combination use first letters
    labels = hashes[:]
    current_index = target_index
    
    while len(labels) > 1:
        next_labels = []
        for i in range(0, len(labels), 2):
            if i + 1 < len(labels):
                left = labels[i]
                right = labels[i + 1]
                if current_index == i:
                    proof.append({"hash": right + "_hash", "position": "right"})
                elif current_index == i + 1:
                    proof.append({"hash": left + "_hash", "position": "left"})
                parent = left[0] + right[0]
                next_labels.append(parent)
            else:
                next_labels.append(labels[i])
        current_index = current_index // 2
        labels = next_labels
    return proof

lines = sys.stdin.read().split('\n')
hashes = lines[0].split(',')
target_index = int(lines[1])
proof = build_proof(hashes, target_index)
print(json.dumps(proof, separators=(',', ':')))