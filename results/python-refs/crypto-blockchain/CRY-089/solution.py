num_inputs = int(input())
num_outputs = int(input())

# P2PKH transaction size estimation
base_size = 10  # version (4) + input_count (1) + output_count (1) + lock_time (4)
input_size = 148  # per input: txid (32) + output_index (4) + script_sig (~107) + sequence (4) + script_length (1)
output_size = 34  # per output: value (8) + script_length (1) + script_pubkey (25)

total_size = base_size + (num_inputs * input_size) + (num_outputs * output_size)

print(total_size)