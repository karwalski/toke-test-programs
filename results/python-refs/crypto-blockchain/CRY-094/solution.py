reserve_x, reserve_y = map(int, input().split())
total_lp_supply = int(input())
deposit_x, deposit_y = map(int, input().split())

lp_tokens = (deposit_x / reserve_x) * total_lp_supply
print(int(lp_tokens))