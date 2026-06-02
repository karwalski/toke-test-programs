bill_amount, tip_percentage, num_people = input().split()
bill_amount = float(bill_amount)
tip_percentage = int(tip_percentage)
num_people = int(num_people)

tip_amount = bill_amount * tip_percentage / 100
total = bill_amount + tip_amount
per_person = total / num_people

print(f"{tip_amount:.2f}")
print(f"{total:.2f}")
print(f"{per_person:.2f}")