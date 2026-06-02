import math

non_witness_size = int(input())
witness_size = int(input())

weight = non_witness_size * 4 + witness_size
virtual_size = math.ceil(weight / 4)

print(weight)
print(virtual_size)