transaction_size = int(input())
fee_rate = int(input())

total_fee_satoshis = transaction_size * fee_rate
total_fee_btc = total_fee_satoshis / 100000000

print(f"{total_fee_btc:.8f}")