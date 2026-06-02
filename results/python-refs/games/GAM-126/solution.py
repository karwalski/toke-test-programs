import sys, random

def main():
    data = sys.stdin.read().split()
    att = int(data[0])
    deff = int(data[1])
    seed = int(data[2])
    random.seed(seed)
    round_num = 0
    lines = []
    while att > 1 and deff > 0:
        round_num += 1
        a_dice_count = min(3, att - 1)
        d_dice_count = min(2, deff)
        a_rolls = sorted([random.randint(1,6) for _ in range(a_dice_count)], reverse=True)
        d_rolls = sorted([random.randint(1,6) for _ in range(d_dice_count)], reverse=True)
        a_loss = 0
        d_loss = 0
        for i in range(min(len(a_rolls), len(d_rolls))):
            if a_rolls[i] > d_rolls[i]:
                d_loss += 1
            else:
                a_loss += 1
        att -= a_loss
        deff -= d_loss
        a_str = '[' + ','.join(str(x) for x in a_rolls) + ']'
        d_str = '[' + ','.join(str(x) for x in d_rolls) + ']'
        lines.append(f'Round {round_num}: ATT{a_str} vs DEF{d_str} -> A-{a_loss} D-{d_loss}')
    if deff == 0:
        result = 'Attacker wins'
    else:
        result = 'Defender wins'
    lines.append(f'Final: Attacker {att}, Defender {deff} - {result}')
    print('\n'.join(lines))

main()
